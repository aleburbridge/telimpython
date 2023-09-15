from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO, join_room

import random

from prompts import prompts
from storyTypes import storyTypes

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
    available_roles = storyTypes.get(story_type, [])
    
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
    return [{"name": player.name, "role": player.role} for player in players]

    
# ------------------- Resource Classes (API Routing) ------------------------

# when "join" or "create game" button is pressed
class PlayerResource(Resource):
    def post(self, name, lobby_code, storyType=None):
        new_player = Player(name, lobby_code)
        if lobby_code in lobbies:
            lobbies[lobby_code]['players'].append(new_player)
        else:
            lobbies[lobby_code] = {'players': [new_player], 'storyType': storyType if storyType else 'Other'}
        return new_player.to_dict(), 201
    
    def get(self, lobby_code):
        if lobby_code not in lobbies:
            return {'error': 'Lobby not found'}, 404
        players = lobbies[lobby_code]['players']
        return [{"name": player.name, "role": player.role} for player in players], 200

class LobbyResource(Resource):
    def post(self):
        lobby_code = generate_lobby_code()
        
        while lobby_code in lobbies:
            lobby_code = generate_lobby_code()
        
        lobbies[lobby_code] = {'players': [], 'storyType': None, 'story': None}
        return {"lobby_code": lobby_code}, 201

# For saving the story to the lobby
class StoryResource(Resource):
    def post(self, lobby_code):
        story = request.json['story']
        if lobby_code not in lobbies:
            return {'error': 'Lobby not found'}, 404
        lobbies[lobby_code]['story'] = story
        socketio.emit('updateStory', {'story': story}, room=lobby_code)
        return {"message": f"Story successfully saved for lobby {lobby_code}: {story}"}, 200

    
class RoleAssignmentResource(Resource):
    def post(self, lobby_code, story_type):
        assign_roles(lobby_code, story_type)

        socketio.emit('start_game', room=lobby_code)
        
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