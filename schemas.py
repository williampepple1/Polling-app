from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_.-]+$')
    role: Literal['admin', 'supervisor', 'voter', 'candidate']

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str]

class CandidateResponse(CandidateCreate):
    id: int

    class Config:
        orm_mode = True

class PollCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str]
    candidates: List[int]  # List of candidate IDs

class PollResponse(PollCreate):
    id: int
    creator_id: int

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    poll_id: int
    candidate_id: int
