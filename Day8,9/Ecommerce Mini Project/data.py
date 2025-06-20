from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mimesis import Person, Generic
from mimesis.locales import Locale
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize database engine & session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Mimesis Generators
generic = Generic(Locale.EN)
person = Person(Locale.EN)

from models import User  # Ensure your SQLAlchemy User model is correctly imported

# Bulk Insert 50,000 Users
users = []
for _ in range(50000):
    user = User(
        username = f"{person.username()}_{generic.random.randint(1000, 9999)}",
        email = f"{person.email().split('@')[0]}_{generic.random.randint(1000, 9999)}@{person.email().split('@')[1]}"
,
        hashed_password="hashed_placeholder",
        gender=person.gender(),
        age=generic.random.randint(18, 65),
        phone_number=person.telephone(),
        nationality=person.nationality(),
        is_active=True
    )
    users.append(user)

# Commit to the database
session.add_all(users)
session.commit()
session.close()

print("50,000 user records inserted successfully!")
