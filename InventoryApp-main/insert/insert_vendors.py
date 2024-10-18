from app import create_app, db
from app.models import Vendor

app = create_app()

vendors = [
    {
        'name': 'Tech Supplies Inc.',
        'contact_person': 'John Doe',
        'phone': '555-1234',
        'email': 'john@techsupplies.com',
        'address': '123 Tech Street, Silicon Valley, CA 94000'
    },
    {
        'name': 'Office Essentials Ltd.',
        'contact_person': 'Jane Smith',
        'phone': '555-5678',
        'email': 'jane@officeessentials.com',
        'address': '456 Office Avenue, Business Park, NY 10001'
    },
    {
        'name': 'Global Gadgets Co.',
        'contact_person': 'Bob Johnson',
        'phone': '555-9876',
        'email': 'bob@globalgadgets.com',
        'address': '789 Gadget Boulevard, Tech City, TX 75001'
    }
]

def insert_vendors():
    with app.app_context():
        for vendor_data in vendors:
            vendor = Vendor(**vendor_data)
            db.session.add(vendor)
        
        db.session.commit()
        print("Vendors inserted successfully!")

if __name__ == '__main__':
    insert_vendors()
