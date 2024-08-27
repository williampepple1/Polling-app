from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from models import User, Poll, Vote
from schemas import UserCreate, PollCreate, VoteCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, role=user.role, password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        return None

def create_poll(db: Session, poll: PollCreate, user_id: int):
    new_poll = Poll(title=poll.title, description=poll.description, created_by=user_id)
    
    if not poll.candidate_ids:
        return None  # A poll must have at least one candidate
    
    candidates = db.query(User).filter(User.id.in_(poll.candidate_ids), User.role == 'candidate').all()
    
    if len(candidates) != len(poll.candidate_ids):
        return None  # Some candidates do not exist
    
    new_poll.candidates = candidates
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)
    return new_poll

def vote_on_poll(db: Session, vote: VoteCreate, user_id: int):
    new_vote = Vote(poll_id=vote.poll_id, voter_id=user_id, candidate_id=vote.candidate_id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote

def get_poll_results(db: Session, poll_id: int):
    votes = db.query(Vote).filter(Vote.poll_id == poll_id).all()
    results = {}
    for vote in votes:
        candidate_name = vote.candidate.username
        if candidate_name in results:
            results[candidate_name] += 1
        else:
            results[candidate_name] = 1
    return results
