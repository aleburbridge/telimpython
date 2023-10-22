from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    room_id = Column("room_id", Integer, ForeignKey('rooms.id'))
    role = Column("role", String)

    def __init__(self, firstname, room_id):
        self.firstname = firstname
        self.room_id = room_id

    def __repr__(self):
        return f"""
          Player {self.id}
          \nFirstname: {self.firstname}
          \nLastname: {self.lastname} {self}
          \nRole: {self.role}"""
    
class Room(Base):
    __tablename__ = "rooms"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    story_type = Column("story_type", String)
    players = relationship("Player", back_populates="room")

    def __init__(self, story_type):
        self.story_type = story_type

    def __repr__(self):
        return f"""
          Room {self.id}"""