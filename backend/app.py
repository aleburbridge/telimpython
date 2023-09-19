from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO, join_room

import random

from story_types import story_types, last_names
from ScriptBuilder import ScriptBuilder

app = Flask(__name__)
api = Api(app)
CORS(app)  
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

lobbies = {} 

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
            'lobby_code': self.lobby_code,
            'role': self.role,
            'assigned_prompts': self.assigned_prompts
        }

# ------------------- Game Logic (Functions) ------------------------

def generate_lobby_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

def assign_roles(lobby_code, story_type):
    available_roles = story_types.get(story_type, [])
    
    if "Host" in available_roles:
        available_roles.remove("Host")
    if "Cohost" in available_roles:
        available_roles.remove("Cohost")

    random.shuffle(available_roles)

    if lobby_code in lobbies:
        players = lobbies[lobby_code]['players']
        if len(players) > len(available_roles) + 2: 
            raise ValueError("Too many players for the selected story type.")
        
        players[0].role = "Host"
        players[0].lastname = random.choice(last_names["Host"])
        players[1].role = "Cohost"
        players[1].lastname = random.choice(last_names["Cohost"])
        
        for idx, player in enumerate(players[2:]):
            if idx < len(available_roles):
                role = available_roles[idx]
                player.role = role
                player.lastname = random.choice(last_names[role])
                
    return [{"name": player.name, "role": player.role, "lastname": player.lastname} for player in players]

def buildScript(lobby_code):
    script_players = [player for player in lobbies[lobby_code]['players']]
    script_story_type = lobbies[lobby_code]['story_type']
    script_story = lobbies[lobby_code]['story']  
    script_builder = ScriptBuilder(script_players, script_story_type, script_story)
    
    final_script = script_builder.build()
    final_script = script_builder.fill_in_initial_script_details() # list of segments
    prompts = script_builder.extract_prompts(final_script)
    
    return final_script, prompts

def assign_prompts_to_players(players, prompts):
    remaining_prompts = prompts.copy()

    for player in players:
        while remaining_prompts:  
            selected_prompt = random.choice(remaining_prompts)

            if selected_prompt["speaker"] != player.role:
                player.assigned_prompts.append(selected_prompt)
                remaining_prompts.remove(selected_prompt)

                if not remaining_prompts:
                    break

            average_prompts_per_player = len(prompts) // len(players)
            if len(player.assigned_prompts) >= average_prompts_per_player:
                break
    
    # leftover prompt assignment
    for prompt in remaining_prompts:
        for player in players:
            if prompt["speaker"] != player.role:
                player.assigned_prompts.append(prompt)
                remaining_prompts.remove(prompt)  
                break


# ------------------- Resource Classes (API Routing) ------------------------

# when "create game" or "join game" is pressed on the home page
class LobbyResource(Resource):
    def post(self):
        lobby_code = generate_lobby_code()
        
        while lobby_code in lobbies:
            lobby_code = generate_lobby_code()
        
        lobbies[lobby_code] = {'players': [], 'story_type': None, 'story': None}
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

        script, prompts = buildScript(lobby_code)
        players = lobbies[lobby_code]['players']

        lobbies[lobby_code]['script'] = script
        lobbies[lobby_code]['prompts'] = prompts

        assign_prompts_to_players(players, prompts)

        return {"message": f"Story successfully saved for lobby {lobby_code}: {story}"}, 200

    
# ------------------ Routes ----------------------------------

@socketio.on('join')
def handle_join(data):
    lobby_code = data['lobbyCode']
    join_room(lobby_code)
    updated_players = [player.to_dict()['name'] for player in lobbies[lobby_code]['players']]
    socketio.emit('updatePlayers', updated_players, room=lobby_code)

# TODO
@socketio.on('player_submitted_prompt')
def handle_prompt_submission():
    print('yup')

api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/', defaults={'story_type': None}, endpoint='player_without_story_type')
api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/<string:story_type>', endpoint='player_with_story_type')
api.add_resource(PlayerResource, '/players/<string:lobby_code>/', endpoint='player_with_role')
api.add_resource(LobbyResource, '/create_lobby')
api.add_resource(RoleAssignmentResource, '/assign_roles/<string:lobby_code>/<string:story_type>')
api.add_resource(StoryResource, '/story/<string:lobby_code>')

# ------------------ Run ----------------------------------
@app.route('/')
def home():
    return 'Hello, Telimpromptu!'

if __name__ == '__main__':
    socketio.run(app, debug=True)