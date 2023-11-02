from flask import Flask
from flask_cors import CORS
import random, string
from database.db_utils import check_room_code_exists, insert_room_code, create_tables

# ------------------- Init ------------------------

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) #TODO: limit origin to react app

# ------------------ Routes -----------------------

@app.route('/api/generate_room_code', methods=['GET'])
def generate_room_code():
    return {
        'room_code': random.randint(1000, 9999)
    }

@app.route('/api/generate_player_id', methods=['GET'])
def generate_player_id():
    return {
        'player_id': ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    }

#TODO: make sure players wihtin lobby cannot have same name

# ------------------ Run --------------------------

if __name__ == '__main__':
    app.run(debug=True) #TODO: turn off when deploying to prod