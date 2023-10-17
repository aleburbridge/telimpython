from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO, join_room
from flask_sqlalchemy import SQLAlchemy
from roles import Role, last_names
from story_types import StoryType, story_type_to_roles
from ScriptBuilder import ScriptBuilder
from routes import initialize_routes

import random

# init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # using SQLite and the database file is named site.db
db = SQLAlchemy(app)
api = Api(app)
CORS(app)  
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

initialize_routes()

lobbies = {} 
# STRUCTURE OF LOBBIES: lobbies[lobby_code] = {'players': [], 'story_type': None, 'story': None, 'answered_prompts': set()}

class Player:
    def __init__(self, name, lobby_code=None, role=None, assigned_prompts=None):
        self.name = name
        self.last_name = None
        self.lobby_code = lobby_code
        self.role = role
        self.assigned_prompts = assigned_prompts or []

    def to_dict(self):
        return {
            'name': self.name,
            'last_name': self.last_name,
            'lobby_code': self.lobby_code,
            'role': self.role,
            'assigned_prompts': self.assigned_prompts
        }

# ------------------- Game Logic ------------------------

def generate_lobby_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

def assign_role_and_last_name(player, role):
    player.role = role
    player.last_name = random.choice(last_names[role.lower()])

def assign_roles(lobby_code, story_type: StoryType):
    available_roles = story_type_to_roles.get(story_type, [])
    special_roles = [Role.HOST, Role.COHOST]

    for role in special_roles:
        if role in available_roles:
            available_roles.remove(role)

    random.shuffle(available_roles)

    if lobby_code in lobbies:
        players = lobbies[lobby_code]['players']

        if len(players) > len(available_roles) + len(special_roles):
            raise ValueError("Too many players for the selected story type.")

        for i, role in enumerate(special_roles):
            assign_role_and_last_name(players[i], role.value)
        
        for i, player in enumerate(players[len(special_roles):]):
            if i < len(available_roles):
                assign_role_and_last_name(player, available_roles[i].value)

def build_script(lobby_code):
    script_players = [player for player in lobbies[lobby_code]['players']]
    script_story_type = lobbies[lobby_code]['story_type']
    script_story = lobbies[lobby_code]['story']  
    script_builder = ScriptBuilder(script_players, script_story_type, script_story)
    
    final_script = script_builder.build()
    final_script = script_builder.fill_in_initial_script_details() # list of segments
    lines_with_prompts = script_builder.extract_lines_with_prompts(final_script)
    return final_script, lines_with_prompts

def assign_prompts_to_players(players, lines_with_prompts):
    remaining_prompts = lines_with_prompts.copy()

    for player in players:
        while remaining_prompts:  
            selected_prompt = random.choice(remaining_prompts)

            if selected_prompt["speaker"].lower() != player.role.lower():
                for prompt in selected_prompt["prompts"]:
                    player.assigned_prompts.append(prompt)
                remaining_prompts.remove(selected_prompt)

                if not remaining_prompts:
                    break

            average_prompts_per_player = len(lines_with_prompts) // len(players)
            if len(player.assigned_prompts) >= average_prompts_per_player:
                break
    
    # leftover prompt assignment
    for prompt in remaining_prompts:
        for player in players:
            if prompt["speaker"] != player.role:
                for extracted_prompt in prompt["prompts"]:
                    player.assigned_prompts.append(extracted_prompt)
                remaining_prompts.remove(prompt)  
                break

def get_dependent_prompts(prompt):
    return [match.split("}")[0][1:] for match in prompt["prompts"]["description"].split("{")[1:]]

# ------------------- Resource Classes ------------------------

# when "create game" or "join game" is pressed on the home page
class LobbyResource(Resource):
    def post(self):
        lobby_code = generate_lobby_code()
        
        while lobby_code in lobbies:
            lobby_code = generate_lobby_code()
        
        lobbies[lobby_code] = {'players': [], 'story_type': None, 'story': None, 'answered_prompts': set()}
        return {"lobby_code": lobby_code}, 201
    
# when player form is filled out 
class PlayerResource(Resource):
    def post(self, name, lobby_code, story_type=None):
        new_player = Player(name, lobby_code)
        if lobby_code in lobbies:
            lobbies[lobby_code]['players'].append(new_player)
        else:
            lobbies[lobby_code] = {'players': [new_player], 'story_type': story_type if story_type else 'Other'}
        return new_player.to_dict(), 201
    
    def get(self, lobby_code):
        if lobby_code not in lobbies:
            return {'error': 'Lobby not found'}, 404
        players = lobbies[lobby_code]['players']
        return [{"name": player.name, "role": player.role} for player in players], 200

class RoleAssignmentResource(Resource):
    def post(self, lobby_code, story_type):
        assign_roles(lobby_code, story_type)

        lobbies[lobby_code]['story_type'] = story_type 
        socketio.emit('start_game', room=lobby_code)
        
        return "Players successfully assigned roles"

class StoryResource(Resource):
    def post(self, lobby_code):
        story = request.json['story']
        if lobby_code not in lobbies:
            return {'error': 'Lobby not found'}, 404
        lobbies[lobby_code]['story'] = story
        socketio.emit('updateStory', story, room=lobby_code)

        script, lines_with_prompts = build_script(lobby_code)
        players = lobbies[lobby_code]['players']
        lobbies[lobby_code]['script'] = script
        lobbies[lobby_code]['prompts'] = lines_with_prompts

        assign_prompts_to_players(players, lines_with_prompts)

        return {"message": f"Story successfully saved for lobby {lobby_code}: {story}"}, 200

    
# ------------------ Socket Events ----------------------------------

@socketio.on('join')
def handle_join(data):
    lobby_code = data['lobbyCode']
    join_room(lobby_code)
    updated_players = [player.to_dict()['name'] for player in lobbies[lobby_code]['players']]
    socketio.emit('updatePlayers', updated_players, room=lobby_code)


@socketio.on('prompt_answered')
def handle_prompt_answered(data):
    lobby_code = data['lobby_code']
    prompt_id = data['prompt_id']
    player_name = data['player_name']
    answered_prompts = lobbies[lobby_code]['answered_prompts']
    answered_prompts.add(prompt_id)
    prompts = lobbies[lobby_code]['prompts']

    available_prompts = []
    for prompt in prompts:
        if prompt["speaker"].lower() == data['player_role'].lower():
            dependencies = get_dependent_prompts(prompt)
            if all(dep in answered_prompts for dep in dependencies):
                available_prompts.append(prompt)

    player = next((p for p in lobbies[lobby_code]['players'] if p.name == player_name), None)

    if player and available_prompts:
        selected_prompt = available_prompts[0]
        player.assigned_prompts.append(selected_prompt)
        
        socketio.emit('new_prompts', player.assigned_prompts, room=request.sid) 

# ------------------ Run ----------------------------------

@app.route('/')
def home():
    return 'Hello, Telimpromptu!'

if __name__ == '__main__':
    socketio.run(app, debug=True)