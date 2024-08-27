from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = Field(..., regex="^(admin|supervisor|voter|candidate)$")

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class PollCreate(BaseModel):
    title: str
    description: str
    candidate_ids: List[int]

class PollResponse(BaseModel):
    id: int
    title: str
    description: str
    candidates: List[UserResponse]

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    poll_id: int
    candidate_id: int
