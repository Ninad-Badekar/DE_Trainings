# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    gender: str
    age: int
    phone_number: str
    nationality: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    gender: str
    age: int
    phone_number: str
    nationality: str
    is_active: bool

    class Config:
        from_attributes = True
