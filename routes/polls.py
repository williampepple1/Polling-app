from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PollCreate, PollResponse, VoteCreate
from database import get_db
from models import Poll  # Import the Poll model
import crud

router = APIRouter()

@router.post("/", response_model=PollResponse)
def create_poll(poll: PollCreate, user_id: int, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_id=user_id)
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Only admins can create polls")
    
    new_poll = crud.create_poll(db, poll, user_id)
    if not new_poll:
        raise HTTPException(status_code=400, detail="Invalid candidates or no candidates provided")
    
    return new_poll

@router.post("/votes/")
def vote_on_poll(vote: VoteCreate, user_id: int, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_id=user_id)
    if user.role != 'voter':
        raise HTTPException(status_code=400, detail="Only voters can vote on polls")
    
    poll = db.query(Poll).filter(Poll.id == vote.poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    if vote.candidate_id not in [candidate.id for candidate in poll.candidates]:
        raise HTTPException(status_code=400, detail="Invalid candidate for this poll")
    
    new_vote = crud.vote_on_poll(db, vote, user_id)
    return new_vote

@router.get("/{poll_id}/results/")
def get_poll_results(poll_id: int, db: Session = Depends(get_db)):
    results = crud.get_poll_results(db, poll_id)
    if not results:
        raise HTTPException(status_code=404, detail="Poll not found")
    return results
