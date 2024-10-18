import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.models import Item, User
from app.extensions import engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Function to insert items from CSV
def insert_items_from_csv(csv_file):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)

    with engine.connect() as connection:
        session = Session(bind=connection)

        try:
            # Fetch user ID to use in items (adjust name based on your data)
            user_result = session.execute(select(User).where(User.name == "Jane Doe")).first()

            if user_result:
                user_id = None

                # Prepare item data from DataFrame
                item_data = []
                for _, row in df.iterrows():
                    # Read values from CSV and set default values for missing ones
                    code = row['Code']
                    description = row['Description']
                    min_quantity = row['Minimum Quantity']

                    # Set default or placeholder values for missing fields
                    quantity = None  # Default starting quantity
                    max_quantity = None  # Example: max quantity is double the minimum
                    qr_code = f"https://example.com/qrcodes/{code}.png"  # Placeholder QR code URL
                    last_order_date = None  # No order date yet
                    last_order_quantity = None  # Default value
                    quantity_updated_at = None
                    start_id = 0 + 1

                    # Set vendor_id to None for now
                    item_data.append({
                        "code": code,
                        "description": description,
                        "quantity": quantity,
                        "minimum_quantity": min_quantity,
                        "max_quantity": max_quantity,
                        "qr_code": qr_code,
                        "last_order_date": last_order_date,
                        "last_order_quantity": last_order_quantity,
                        "quantity_last_updated_by": user_id,
                        "quantity_updated_at": quantity_updated_at,  # Add this line
                        "stock_status": None,
                        "reorder_quantity": None,
                        "vendor_id": None  # Set vendor_id to None for now
                    })

                # Insert item data
                session.execute(insert(Item), item_data)
                session.commit()
                print("Items inserted successfully.")
            else:
                print("User not found. Please check your data.")

        except Exception as e:
            print("Error inserting items:", e)
            session.rollback()

# Run the function
if __name__ == "__main__":
    csv_file = "Inventory.csv"  # Replace with your actual CSV file name
    insert_items_from_csv(csv_file)
