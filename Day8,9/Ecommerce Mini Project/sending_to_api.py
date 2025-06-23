import os
import requests
import time
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import User  # Make sure User is defined correctly in models.py

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# API endpoint
API_URL = "http://127.0.0.1:8000/users/"

# Configure logging
logging.basicConfig(
    filename="sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Fetch users from the database in batches
def fetch_users(batch_size=10, offset=0):
    try:
        with SessionLocal() as session:
            users = session.query(User).offset(offset).limit(batch_size).all()
            return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return []

# Send a batch of users to the FastAPI server
def send_users_to_api(users):
    success = True
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "gender": user.gender,
            "age": user.age,
            "phone_number": user.phone_number,
            "nationality": user.nationality,
            "is_active": user.is_active,
            "created_at": str(user.created_at) if hasattr(user, "created_at") else None
        }
        try:
            response = requests.post(API_URL, json=user_dict)
            if response.status_code not in [200, 201]:
                success = False
        except requests.RequestException as e:
            logger.error(f"Request error for user {user.username}: {str(e)}")
            success = False
    return success

# Save current offset to track syncing progress
def save_progress(offset):
    with open("sync_progress.txt", "w") as f:
        f.write(str(offset))

# Load previously saved offset
def load_progress():
    try:
        with open("sync_progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

# Main process
if __name__ == "__main__":
    batch_size = 1000
    total_records = 50000  # Replace with real total if needed
    sync_interval = 10  # In seconds
    offset = load_progress()
    processed_count = offset

    logger.info("Starting synchronization process...")

    while offset < total_records:
        users_to_send = fetch_users(batch_size, offset)
        if users_to_send:
            success = send_users_to_api(users_to_send)
            if success and processed_count == 0:
                logger.info("Initial connection to FastAPI successful.")

            offset += batch_size
            processed_count += batch_size
            save_progress(offset)

            if processed_count % 10000 == 0:
                logger.info(f"Processed {processed_count} users so far.")
        else:
            logger.info("No users left to process.")
            break

        time.sleep(sync_interval)
