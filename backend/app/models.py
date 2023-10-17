from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    room_code = db.Column(db.String(4), db.ForeignKey('room.room_code'))
    role = db.Column(db.String(20))
    prompt_ids = db.relationship('PromptIds', secondary='player_prompt_association')

class Room(db.Model):
    room_code = db.Column(db.String(10), primary_key=True, unique=True)
    story_type = db.Column(db.String(50))
    story = db.Column(db.String(500))
    players = db.relationship('Player', backref='room', lazy=True)
    answered_prompt_ids = db.relationship('PromptIds', secondary='room_prompt_association')
    

class PromptIds(db.Model):
    id = db.Column(db.String(50), primary_key=True, unique=True)

player_prompt_association = db.Table('player_prompt_association',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
    db.Column('prompt_id', db.String, db.ForeignKey('prompt_ids.id'))
)

room_prompt_association = db.Table('room_prompt_association',
    db.Column('room_code', db.String, db.ForeignKey('room.room_code')),
    db.Column('prompt_id', db.String, db.ForeignKey('prompt_ids.id'))
)