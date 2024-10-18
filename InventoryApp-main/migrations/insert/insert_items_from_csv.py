import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.models import engine
from datetime import datetime
from app.models.user import User
from app.models.item import Item

# Load environment variables
load_dotenv()

# Function to insert items from CSV
def insert_items_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    with engine.connect() as connection:
        session = Session(bind=connection)

        try:
            # Fetch user ID to use in items (adjust name based on your data)
            user = session.execute(select(User).where(User.name == "Jane Doe")).first()

            if user:
                
                item_data = []
                for _, row in df.iterrows():
                    code = row['Code']
                    description = row['Description']
                    min_quantity = row['Minimum Quantity']

                    item_data.append({
                        "code": code,
                        "description": description,
                        "quantity": None,
                        "minimum_quantity": min_quantity,
                        "max_quantity": None,
                    
                    
                        "qr_code": f"https://example.com/qrcodes/{code}.png",
                        "last_order_date": None,
                        "last_order_quantity": None,
                       
                        "quantity_last_updated_by": None,
                        "quantity_updated_at": None,
                        "stock_status": None,
                        "reorder_quantity": None,
                        "vendor_id": None
                    })

                session.execute(insert(Item), item_data)
                session.commit()
                print("Items inserted successfully.")
            else:
                print("User 'Jane Doe' not found. Please check your data.")

        except Exception as e:
            print("Error inserting items:", e)
            session.rollback()

# Run the function
if __name__ == "__main__":
    csv_file = "Inventory.csv"  # Replace with your actual CSV file name
    insert_items_from_csv(csv_file)
