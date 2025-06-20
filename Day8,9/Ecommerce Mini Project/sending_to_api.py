import os
import requests
import logging
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import User  # Import User model from models.py

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
    filename="sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def fetch_users(batch_size=10, offset=0):
    """ Fetch users in batches of `batch_size`, using offset """
    try:
        with SessionLocal() as session:
            users = session.query(User).offset(offset).limit(batch_size).all()
            logger.info(f"Fetched {len(users)} users from database (Offset: {offset}).")
            return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return []

def send_users_to_api(users):
    """ Send user data to FastAPI """
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
            "is_active": user.is_active
        }

        try:
            response = requests.post(API_URL, json=user_dict)
            if response.status_code == 200:
                logger.info(f"User {user.username} added successfully.")
            elif response.status_code == 201:
                logger.info(f"User {user.username} created successfully.")
            else:
                logger.warning(f"Failed to add {user.username}: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            logger.error(f"Error sending data to API for user {user.username}: {str(e)}")

def save_progress(offset):
    """ Save the current offset to a file """
    with open("sync_progress.txt", "w") as f:
        f.write(str(offset))

def load_progress():
    """ Load the last saved offset from a file """
    try:
        with open("sync_progress.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

if __name__ == "__main__":
    batch_size = 1000
    total_records = 50000  # Your total dataset size
    sync_interval = 10  # Runs every 10 seconds
    offset = load_progress()  # Track progress

    logger.info(f"Starting process to send {total_records} users in batches of {batch_size} every {sync_interval} seconds.")

    while offset < total_records:
        users_to_send = fetch_users(batch_size, offset)
        if users_to_send:
            send_users_to_api(users_to_send)
            offset += batch_size  # Move to the next batch
            save_progress(offset)  # Save progress
        else:
            logger.info("No users left to process.")
            break  # Stop execution once all records are sent
        
        time.sleep(sync_interval)  # Wait before processing next batch
