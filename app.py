from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO, join_room

import random

from prompts import prompts
from categories import categories

app = Flask(__name__)
api = Api(app)
CORS(app)  
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])

lobbies = {} 

class Player:
    def __init__(self, name, lobby_code=None, role=None, assigned_prompts=None):
        self.name = name
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
    available_roles = categories.get(story_type, [])
    
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
        players[1].role = "Cohost"
        
        for idx, player in enumerate(players[2:]):
            if idx < len(available_roles):
                role = available_roles[idx]
                player.role = role
        print("ROLES ASSIGNED!!!!")
        print(players)
    return [{"name": player.name, "role": player.role} for player in players]

    
# ------------------- Resource Classes (API Routing) ------------------------
class PlayerResource(Resource):
    def post(self, name, lobby_code, storyType=None):
        new_player = Player(name, lobby_code)
        if lobby_code in lobbies:
            if storyType and lobbies[lobby_code]['storyType'] != storyType:
                return {"error": "Cannot change the storyType for an existing lobby."}, 400
            lobbies[lobby_code]['players'].append(new_player)
        else:
            lobbies[lobby_code] = {'players': [new_player], 'storyType': storyType if storyType else 'Other'}
        return new_player.to_dict(), 201

    
class LobbyResource(Resource):
    def post(self):
        lobby_code = generate_lobby_code()
        
        while lobby_code in lobbies:
            lobby_code = generate_lobby_code()
        
        lobbies[lobby_code] = {'players': [], 'storyType': None}
        return {"lobby_code": lobby_code}, 201
    
class RoleAssignmentResource(Resource):
    def post(self, lobby_code, story_type):
        assign_roles(lobby_code, story_type)
        
        return "Players successfully assigned roles"

# ------------------ Routes ----------------------------------
@socketio.on('join')
def handle_join(data):
    lobby_code = data['lobbyCode']
    join_room(lobby_code)
    updated_players = [player.to_dict()['name'] for player in lobbies[lobby_code]['players']]
    socketio.emit('updatePlayers', updated_players, room=lobby_code)

api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/', defaults={'storyType': None}, endpoint='player_without_storyType')
api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/<string:storyType>', endpoint='player_with_storyType')
api.add_resource(LobbyResource, '/create_lobby')
api.add_resource(RoleAssignmentResource, '/assign_roles/<string:lobby_code>/<string:storyType>')

# ------------------ Run ----------------------------------
@app.route('/')
def home():
    return 'Hello, Telimpromptu!'

if __name__ == '__main__':
    socketio.run(app, debug=True)