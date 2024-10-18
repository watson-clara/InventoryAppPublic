from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DECIMAL, TIMESTAMP, Date, DateTime, ForeignKey, select
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the vendors table
vendors = Table('vendors', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('contact_info', Text),
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('updated_at', TIMESTAMP, default=func.now(), onupdate=func.now())
)

# Update the users table definition
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('password', String(255), nullable=False),  # Store hashed passwords
    Column('role', String(50), nullable=False),  # User role, e.g., "admin", "manager", "staff"
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('updated_at', TIMESTAMP, default=func.now(), onupdate=func.now())
)

# Create the tables in the database
try:
    metadata.create_all(engine)
    print("Tables created successfully.")
except Exception as e:
    print("Error creating tables:", e)

# Create the tables in the database
try:
    metadata.create_all(engine)
    print("Tables created successfully.")
except Exception as e:
    print("Error creating tables:", e)


# Define the items table with the updated fields
items = Table('items', metadata,
    Column('code', String(50), primary_key=True),
    Column('qr_code', String(255)),  # QR code link for updating quantity
    Column('description', Text),
    Column('quantity', Integer, nullable=True),
    Column('minimum_quantity', Integer, nullable=True),
    Column('max_quantity', Integer, nullable=True),
    Column('vendor_id', Integer, ForeignKey('vendors.id'), nullable=True),  # Foreign key to vendors table
    Column('last_order_date', Date, nullable=True),
    Column('last_order_quantity', Integer, nullable=True),
    Column('quantity_updated_at', DateTime, default=func.now(), onupdate=func.now()),
    Column('quantity_last_updated_by', Integer, ForeignKey('users.id'), nullable=True),  # Foreign key to users table
    Column('stock_status', String(20), nullable=True),
    Column('reorder_quantity', Integer, nullable=True), 
)


# Function to calculate stock status and reorder quantity
def calculate_stock_status_and_reorder_quantity(quantity, min_quantity, max_quantity):
    stock_status = "In Stock" if quantity > min_quantity else "Low Stock"
    reorder_quantity = max(0, max_quantity - quantity) if quantity <= min_quantity else 0
    return stock_status, reorder_quantity

# Function to retrieve low stock items
def get_low_stock_items():
    with engine.connect() as connection:
        session = Session(bind=connection)

        # Query for items with "Low Stock" status
        low_stock_items_query = select(items).where(items.c.stock_status == "Low Stock")
        low_stock_items = session.execute(low_stock_items_query).fetchall()

        # Display the low stock items
        for item in low_stock_items:
            print(f"Code: {item.code}, Name: {item.name}, Quantity: {item.quantity}, Minimum Quantity: {item.minimum_quantity}")

# Create the tables in the database
try:
    metadata.create_all(engine)
    print("Tables created successfully.")
except Exception as e:
    print("Error creating tables:", e)

# Example usage of get_low_stock_items function
if __name__ == "__main__":
    get_low_stock_items()
