from .db import db, environment, SCHEMA
from datetime import datetime

class Child(db.Model):
    __tablename__ = 'children'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    skill_level = db.Column(db.String(20), nullable=True)
    progress = db.Column(db.JSON, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'date_of_birth': self.date_of_birth.isoformat(),
            'skill_level': self.skill_level,
            'progress': self.progress,
            'parent_id': self.parent_id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
