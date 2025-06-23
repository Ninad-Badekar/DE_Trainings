import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App and password hashing
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    gender: str
    age: int
    phone_number: str
    nationality: str
    is_active: bool = True
    created_at: datetime = datetime.now()

# In-memory database
users_db: List[User] = []

# Password utilities
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Routes
@app.post("/users/", response_model=User)
def create_user(user: User):
    if any(u.username == user.username or u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="User already exists")
    user.hashed_password = hash_password(user.hashed_password)
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
def list_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
