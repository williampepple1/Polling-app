from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

poll_candidates = Table(
    'poll_candidates',
    Base.metadata,
    Column('poll_id', Integer, ForeignKey('polls.id')),
    Column('candidate_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # hashed password
    role = Column(String)  # 'admin', 'supervisor', 'voter', 'candidate'

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User")
    candidates = relationship("User", secondary=poll_candidates)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey('polls.id'))
    voter_id = Column(Integer, ForeignKey('users.id'))
    candidate_id = Column(Integer, ForeignKey('users.id'))
    vote_choice = Column(String)

    poll = relationship("Poll")
    voter = relationship("User", foreign_keys=[voter_id])
    candidate = relationship("User", foreign_keys=[candidate_id])
