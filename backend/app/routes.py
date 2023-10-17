from flask_restful import Api
from app import api  
from app import PlayerResource, LobbyResource, RoleAssignmentResource, StoryResource  

def initialize_routes():
    api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/', defaults={'story_type': None}, endpoint='player_without_story_type')
    api.add_resource(PlayerResource, '/player/<string:lobby_code>/<string:name>/<string:story_type>', endpoint='player_with_story_type')
    api.add_resource(PlayerResource, '/players/<string:lobby_code>/', endpoint='player_with_role')
    api.add_resource(LobbyResource, '/create_lobby')
    api.add_resource(RoleAssignmentResource, '/assign_roles/<string:lobby_code>/<string:story_type>')
    api.add_resource(StoryResource, '/story/<string:lobby_code>')
