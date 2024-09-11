# models/course_request.py
from .db import db, environment, SCHEMA
from datetime import datetime

class CourseRequest(db.Model):
    __tablename__ = 'course_requests'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    downvotes = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='idle')  # idle, working on, launched
    opted_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requested_by': self.requested_by,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'status': self.status,
            'opted_by': self.opted_by,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
