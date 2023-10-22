from flask import jsonify
from flask_restful import Api
from config import app, db
from database.models import Player, Room
from database.init_db import init_db

database_session = init_db()

@app.route('/')
def home():
    return '📺'

@app.route('/create_room/<string:story_type>', methods=['POST'])
def create_room(story_type):
    new_room = Room(
        story_type=story_type
    )
    database_session.add(new_room)
    database_session.commit()

@app.route('/create_player/<string:name>/<string:room_code>', methods=['POST'])
def add_player(name, room_code):
    if not name or not room_code:
        return jsonify({"error": "Name and room_code are required to add a player"}), 400
    
    new_player = Player(
        name=name, 
        room_code=room_code,
    )
    db.session.add(new_player)
    db.session.commit()

    return jsonify({"message": "Player added", "player_id": new_player.id}), 201

'''
@app.route('/assign_roles/<string:room_code>', methods=['POST'])
def assign_roles(room_code):
    return "Nice"
'''