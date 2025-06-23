import os
import requests
import logging
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, text
from sqlalchemy.dialects.mysql import insert
from dotenv import load_dotenv
from models import Base

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
API_URL = "http://127.0.0.1:8000/users/"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Logging configuration
logging.basicConfig(
    filename="new_sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Define MySQL models
class NewUser(Base):
    __tablename__ = 'new_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    nationality = Column(String(100), nullable=False)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

class SyncTracker(Base):
    __tablename__ = "sync_tracker"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_synced_at = Column(DateTime, server_default=func.now())

Base.metadata.create_all(bind=engine)

# Get last sync time
def get_last_sync_time():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT MAX(last_synced_at) FROM sync_tracker")).scalar()
        return result or "2025-01-01 00:00:00"
    finally:
        session.close()

# Update sync timestamp
def update_sync_timestamp():
    session = SessionLocal()
    try:
        session.execute(text("INSERT INTO sync_tracker (last_synced_at) VALUES (CURRENT_TIMESTAMP)"))
        session.commit()
    finally:
        session.close()

# Fetch updated users from the API
def fetch_users_from_api(since_timestamp):
    try:
        response = requests.get(API_URL, params={"updated_after": since_timestamp}, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Failed to fetch users: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
    return []

# Upsert into MySQL
def upsert_users(users):
    session = SessionLocal()
    try:
        count = 0
        for user in users:
            stmt = insert(NewUser).values(**user).on_duplicate_key_update(
                username=user["username"],
                email=user["email"],
                hashed_password=user["hashed_password"],
                gender=user["gender"],
                age=user["age"],
                phone_number=user["phone_number"],
                nationality=user["nationality"],
                created_at=user["created_at"],
                is_active=user["is_active"]
            )
            session.execute(stmt)
            count += 1
        session.commit()
        if count:
            logger.info(f"{count} users inserted or updated.")
        return count
    except Exception as e:
        session.rollback()
        logger.error(f"Error during upsert: {str(e)}")
        return 0
    finally:
        session.close()

# Main loop
if __name__ == "__main__":
    sync_interval = 10  # seconds
    logger.info(f"Starting incremental sync every {sync_interval} seconds...")

    while True:
        last_sync = get_last_sync_time()
        users = fetch_users_from_api(last_sync)
        if users:
            upsert_users(users)
            update_sync_timestamp()
        else:
            logger.info("No new or updated users fetched.")
        time.sleep(sync_interval)
