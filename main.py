from fastapi import FastAPI
from database import engine, Base
from routes import users, polls

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(polls.router, prefix="/polls", tags=["Polls"])
