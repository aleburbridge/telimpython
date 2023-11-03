from flask import Flask
from flask_cors import CORS
import random, string
from database.db_utils import database_has_room_code, insert_room_code, create_tables

# ------------------- Init ------------------------

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #TODO: limit origin to react app
create_tables()

# ------------------ Routes -----------------------

@app.route('/api/generate_room_code', methods=['GET'])
def generate_room_code():
    while True:
        room_code = random.randint(1000, 9999)
        if not database_has_room_code(room_code):
            insert_room_code(room_code)
            return {
                'room_code': room_code
            }

@app.route('/api/generate_player_id', methods=['GET'])
def generate_player_id():
    player_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return {
        'player_id': player_id
    }

#TODO: make sure players wihtin lobby cannot have same name

# ------------------ Run --------------------------

if __name__ == '__main__':
    app.run(debug=True) #TODO: turn off when deploying to prod