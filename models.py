from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  
    role = Column(String) 

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey('polls.id'))
    voter_id = Column(Integer, ForeignKey('users.id'))
    vote_choice = Column(String)

    poll = relationship("Poll")
    voter = relationship("User")
