import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Secret & algorithm for JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Missing JWT_SECRET_KEY environment variable")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
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
    created_at: datetime = Field(default_factory=datetime.now)

class UserInDB(User):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# In-memory user store
users_db: List[UserInDB] = []

# Utility functions
def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(username: str) -> Optional[UserInDB]:
    return next((u for u in users_db if u.username == username), None)

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Your authentication logic here
    return {"access_token": "your_jwt_token", "token_type": "bearer"}

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exc = HTTPException(
        status_code=401, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exc
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exc
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exc
    return user

# Protected routes
@app.post("/users/", response_model=User)
async def create_user(user: User, current_user: UserInDB = Depends(get_current_user)):
    if any(u.username == user.username or u.email == user.email or u.phone_number == user.phone_number for u in users_db):
        raise HTTPException(status_code=400, detail="User already exists")
    user.hashed_password = get_password_hash(user.hashed_password)
    users_db.append(UserInDB(**user.dict()))
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: UserInDB = Depends(get_current_user)):
    for u in users_db:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/", response_model=List[User])
async def list_users(current_user: UserInDB = Depends(get_current_user)):
    return users_db
