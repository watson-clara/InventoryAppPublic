from app.extensions import db
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'items'
    code = db.Column(db.String(100),primary_key=True, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=True)
    minimum_quantity = db.Column(db.Integer, nullable=True)
    max_quantity = db.Column(db.Integer, nullable=True)
    last_order_date = db.Column(db.DateTime, nullable=True)
    last_order_quantity = db.Column(db.Integer, nullable=True)
    quantity_last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    quantity_updated_at = db.Column(db.DateTime, default=datetime.now)
    stock_status = db.Column(db.String(50), nullable=True)
    reorder_quantity = db.Column(db.Integer, nullable=True) 
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)

    vendor = relationship('Vendor', back_populates='items')
    quantity_updater = relationship('User', foreign_keys=[quantity_last_updated_by])

    @validates('quantity')
    def update_stock_status(self, key, quantity):
        if quantity is not None and self.minimum_quantity is not None:
            if quantity <= self.minimum_quantity:
                self.stock_status = 'Low Stock'
            else:
                self.stock_status = 'In Stock'
        else:
            self.stock_status = 'Unknown'
        return quantity

    

    def __repr__(self):
        return f'<Item {self.code}>'

    def update_order_info(self, order_quantity):
        self.last_order_date = datetime.now()
        self.last_order_quantity = order_quantity
        self.quantity += order_quantity

@event.listens_for(Item, 'before_insert')
@event.listens_for(Item, 'before_update')
def calculate_fields(mapper, connection, target):
    # Calculate reorder quantity
    if target.quantity is not None and target.minimum_quantity is not None and target.max_quantity is not None:
        if target.quantity <= target.minimum_quantity:
            target.reorder_quantity = target.max_quantity - target.quantity
        else:
            target.reorder_quantity = 0
    else:
        target.reorder_quantity = 0

    


