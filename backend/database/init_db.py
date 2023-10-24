from sqlalchemy import  create_engine, text
from sqlalchemy.orm import sessionmaker
from database.models import Base, Room

def init_db():
    engine = create_engine("sqlite:///db.db", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session