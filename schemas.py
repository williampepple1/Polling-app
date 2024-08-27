from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = Field(..., regex="^(admin|supervisor|candidate|voter)$")

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class PollCreate(BaseModel):
    title: str
    description: str

class VoteCreate(BaseModel):
    poll_id: int
    vote_choice: str
