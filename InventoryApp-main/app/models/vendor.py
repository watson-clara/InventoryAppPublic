from app.extensions import db
from sqlalchemy.orm import relationship

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    
    items = relationship('Item', back_populates='vendor')

    def __repr__(self):
        return f'<Vendor {self.name}>'

