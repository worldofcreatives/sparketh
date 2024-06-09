from .db import db, environment, SCHEMA
from datetime import datetime

class Parent(db.Model):
    __tablename__ = 'parents'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    address_1 = db.Column(db.String(100), nullable=True)
    address_2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    stripe_customer_id = db.Column(db.String(50), nullable=True)
    stripe_subscription_id = db.Column(db.String(50), nullable=True)
    children = db.relationship('Student', backref='parent', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profile_pic': self.profile_pic,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'stripe_customer_id': self.stripe_customer_id,
            'stripe_subscription_id': self.stripe_subscription_id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
