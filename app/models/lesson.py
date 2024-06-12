from .db import db, environment, SCHEMA
from datetime import datetime

class Lesson(db.Model):
    __tablename__ = 'lessons'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'course_id': self.course_id,
            'url': self.url,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
