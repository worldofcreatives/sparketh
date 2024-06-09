# teacher.py

from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Teacher(db.Model):
    __tablename__ = 'teachers'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False, unique=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address_1 = db.Column(db.String(100), nullable=False)
    address_2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    expertise = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User
    user = db.relationship('User', backref=db.backref('teacher', uselist=False, lazy=True))

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
            'bio': self.bio,
            'expertise': self.expertise,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
