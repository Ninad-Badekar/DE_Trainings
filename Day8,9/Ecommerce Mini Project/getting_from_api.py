import os
import requests
import logging
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, text
from dotenv import load_dotenv
from models import Base  # Import Base from models.py

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# FastAPI API endpoint
API_URL = "http://127.0.0.1:8000/users/"

# Setup logging
logging.basicConfig(
    filename="new_sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Define new MySQL table to store API data
class NewUser(Base):
    __tablename__ = 'new_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    nationality = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

# Create new table if not exists
Base.metadata.create_all(bind=engine)

# Track sync time for incremental loading
class SyncTracker(Base):
    __tablename__ = "sync_tracker"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_synced_at = Column(DateTime, server_default=func.now())

Base.metadata.create_all(bind=engine)

def get_last_sync_time():
    """ Fetch the last sync timestamp or insert a default one """
    session = SessionLocal()
    try:
        last_sync = session.execute(text("SELECT MAX(last_synced_at) FROM sync_tracker")).scalar()
        if last_sync is None:
            last_sync = "2025-01-01 00:00:00"  # Adjust this to match real data
            session.execute(text("INSERT INTO sync_tracker (last_synced_at) VALUES (:sync_time)"), {"sync_time": last_sync})
            session.commit()
            logger.info(f"Initialized sync_tracker with timestamp: {last_sync}")
        return last_sync
    except Exception as e:
        logger.error(f"Error fetching last sync timestamp: {str(e)}")
        return "2025-01-01 00:00:00"
    finally:
        session.close()

def fetch_users_from_api():
    """ Fetch users from FastAPI with incremental load """
    last_sync = get_last_sync_time()
    try:
        response = requests.get(f"{API_URL}?created_after={last_sync}", timeout=5)  # Set timeout for API requests
        if response.status_code == 200:
            users = response.json()
            logger.info(f"Fetched {len(users)} new users from API since last sync ({last_sync}).")
            return users
        else:
            logger.warning(f"Failed to fetch users: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return []

def insert_users_into_mysql(users):
    """ Insert API users into MySQL table with error handling """
    session = SessionLocal()
    try:
        for user in users:
            existing_user = session.query(NewUser).filter_by(email=user["email"]).first()
            if existing_user:
                logger.info(f"User {user['username']} already exists. Skipping.")
                continue

            new_user = NewUser(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                hashed_password=user["hashed_password"],
                gender=user["gender"],
                age=user["age"],
                phone_number=user["phone_number"],
                nationality=user["nationality"],
                is_active=user["is_active"]
            )
            session.add(new_user)
        
        session.commit()
        logger.info(f"Inserted {len(users)} users into MySQL table.")

        # Update sync tracker timestamp
        session.execute(text("INSERT INTO sync_tracker (last_synced_at) VALUES (CURRENT_TIMESTAMP)"))
        session.commit()

    except Exception as e:
        logger.error(f"Error inserting users into MySQL: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    sync_interval = 10  # Runs every 10 seconds
    logger.info(f"Starting incremental data transfer process every {sync_interval} seconds.")

    while True:
        users_from_api = fetch_users_from_api()
        if users_from_api:
            insert_users_into_mysql(users_from_api)
        else:
            logger.info("No new users fetched from API.")
        
        time.sleep(sync_interval)  # Wait before next batch
