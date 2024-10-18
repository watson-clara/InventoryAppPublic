from sqlalchemy import insert
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from app.models import Item, User
from app.extensions import engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Function to add users to the database
def add_users():
    user_data = [
        {"name": "Jane Doe", "email": "jane.doe@example.com", "password": generate_password_hash("password123"), "role": "admin"},
        {"name": "John Smith", "email": "john.smith@example.com",  "password": generate_password_hash("password456"), "role": "manager"},
        {"name": "Alice Johnson", "email": "alice.johnson@example.com",  "password": generate_password_hash("password789"), "role": "staff"}
    ]

    with engine.connect() as connection:
        session = Session(bind=connection)
        try:
            # Insert user data
            session.execute(insert(User), user_data)
            session.commit()
            print("Users added successfully.")
        except Exception as e:
            print("Error adding users:", e)
            session.rollback()

# Run the function
if __name__ == "__main__":
    add_users()
