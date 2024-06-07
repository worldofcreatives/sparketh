from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    creators = db.relationship('Creator', backref='company', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'bio': self.bio,
            'logo': self.logo,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'creators': [creator.to_dict() for creator in self.creators]
        }
