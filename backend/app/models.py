from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(26), nullable=False)
    lobby_code = db.Column(db.Integer(4), db.ForeignKey('lobby.lobby_code'))

    # ... rest of your Player class

class Lobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lobby_code = db.Column(db.String(10), unique=True)
    story_type = db.Column(db.String(50))
    story = db.Column(db.String(500))
    
    players = db.relationship('Player', backref='lobby', lazy=True)
    answered_prompts = db.Column(db.String(500))  # Storing as comma-separated; consider better options
    
    # ... Initialize as needed