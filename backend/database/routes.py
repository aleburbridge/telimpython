from flask import Blueprint
from database.models import Player, Room
from database.init_db import init_db

database_session = init_db()
bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return '📺'

@bp.route('/create_room/<string:story_type>', methods=['POST'])
def create_room(story_type):
    new_room = Room(
        story_type=story_type
    )
    database_session.add(new_room)
    database_session.commit()

@bp.route('/create_player/<string:name>/<string:room_code>', methods=['POST'])
def add_player(name, room_code):
    new_player = Player(
        name=name, 
        room_code=room_code,
    )
    database_session.add(new_player)
    database_session.commit()

'''
@app.route('/assign_roles/<string:room_code>', methods=['POST'])
def assign_roles(room_code):
    return "Nice"
'''