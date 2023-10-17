from flask import Flask, jsonify
from flask_restful import Api
from app import app, db, api, generate_player_code, generate_room_code
from models import Player, Room

@app.route('/get_room_code', methods=['GET'])
def get_room_code():
    return generate_room_code()

@app.route('/create_room/<string:room_code>/<string:story_type>', methods=['POST'])
def create_room(room_code, story_type):
    all_room_codes = [room.room_code for room in Room.query.all()] # TODO: cache this somehow
    while room_code in all_room_codes:
        # there are 10,000 possible 4 digit combinations so I think this is very unlikely to happen and will result in the room code seen on room creation to differ from the actual room code, but that's not a big deal since the correct one will display on the next page. Maybe there's a better way to do this
        room_code = generate_room_code()
    
    new_room = Room(
        room_code=room_code,
        story_type=story_type
    )
    db.session.add(new_room)
    db.session.commit()

@app.route('/create_player/<string:name>/<string:room_code>', methods=['POST'])
def add_player(name, room_code):
    if not name or not room_code:
        return jsonify({"error": "Name and room_code are required to add a player"}), 400
    
    new_player = Player(
        id=generate_player_code(), 
        name=name, 
        room_code=room_code,
    )
    db.session.add(new_player)
    db.session.commit()

    return jsonify({"message": "Player added", "player_id": new_player.id}), 201

@app.route('/assign_roles/<string:room_code>', methods=['POST'])
def assign_roles(room_code):
    return "Nice"