import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base, User  # Your existing SQLAlchemy models
from datetime import datetime

# Load .env
load_dotenv()

# Setup SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# API endpoint
API_URL = "http://localhost:8000/users"  # or your actual endpoint

def get_latest_user_created_at(session):
    """Get the latest user creation timestamp from the DB."""
    latest = session.query(User).order_by(User.created_at.desc()).first()
    return latest.created_at if latest else None

def fetch_users_from_api():
    """Fetch all users from API."""
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def load_incremental_users():
    session = SessionLocal()
    try:
        latest_ts = get_latest_user_created_at(session)
        print(f"🔍 Latest user in DB created at: {latest_ts}")

        api_users = fetch_users_from_api()
        new_users = []

        for user in api_users:
            user_ts = datetime.fromisoformat(user["created_at"])
            if not latest_ts or user_ts > latest_ts:
                new_users.append(User(
                    username=user["username"],
                    email=user["email"],
                    hashed_password=user["hashed_password"],
                    gender=user["gender"],
                    age=user["age"],
                    phone_number=user["phone_number"],
                    nationality=user["nationality"],
                    is_active=user["is_active"],
                    created_at=user_ts
                ))

        print(f"✅ Found {len(new_users)} new users to insert.")

        if new_users:
            session.add_all(new_users)
            session.commit()
            print("🎉 New users inserted successfully.")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        session.close()

if __name__ == "__main__":
    load_incremental_users()
