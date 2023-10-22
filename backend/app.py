from flask import request
from flask_socketio import join_room
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from script_building.roles import Role, last_names
from script_building.story_types import StoryType, story_type_to_roles
from script_building.ScriptBuilder import ScriptBuilder

from database.routes import bp

import random, string

# ------------------- Init ------------------------

app = Flask(__name__)
app.register_blueprint(bp)
CORS(app)  
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

# ------------------- Game Logic ------------------------

def generate_room_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

def generate_player_code():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

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
if __name__ == '__main__':
    socketio.run(app, debug=True)