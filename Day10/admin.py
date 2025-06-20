from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User, Base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime

# Setup
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session = Session(bind=engine)

# Insert admin user
hashed_pw = pwd_context.hash("Test1234@")

user = User(
    username="admin123",
    email="admin@example.com",
    hashed_password=hashed_pw,
    gender="Male",
    age=25,
    phone_number="91234567239",
    nationality="Indian",
    created_at=datetime.now(),
    is_active=True
    
)

session.add(user)
session.commit()
session.close()
print("✅ Admin user created successfully.")
