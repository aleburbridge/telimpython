import sqlite3
from flask import Blueprint, jsonify
from database.models import Player, Room
from database.init_db import init_db
import random, string

database_session = init_db()
bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return '📺'

@bp.route('/get_room_code', methods=['GET'])
def get_room_code():
    while True:
        room_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
        existing_room = database_session.query(Room).filter_by(id=room_code).first()
        
        if existing_room is None:
            break
    
    return jsonify({"room_code": room_code})

@bp.route('/create_room/<string:room_code>/<string:story_type>', methods=['POST'])
def create_room(room_code, story_type):
    new_room = Room(
        id=room_code,
        story_type=story_type,
    )
    database_session.add(new_room)
    database_session.commit()

    return jsonify({"status": "success", "message": "Room created"}), 201


@bp.route('/create_player/<string:name>/<string:room_code>', methods=['POST'])
def add_player(name, room_code):
    new_player = Player(
        firstname=name, 
        room_code=room_code,
    )
    database_session.add(new_player)
    database_session.commit()

'''
@app.route('/assign_roles/<string:room_code>', methods=['POST'])
def assign_roles(room_code):
    return "Nice"
'''