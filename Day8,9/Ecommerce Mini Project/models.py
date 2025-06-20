from sqlalchemy import create_engine,Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize base and engine
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)  # Added phone number
    nationality = Column(String(100), nullable=False)  # Added nationality
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

# Create tables
Base.metadata.create_all(engine)
