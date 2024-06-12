from .db import db, environment, SCHEMA
from datetime import datetime

class Track(db.Model):
    __tablename__ = 'tracks'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=True)
    outcomes = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    downloadable_files = db.Column(db.JSON, nullable=True)

    teacher = db.relationship('Teacher', backref=db.backref('tracks', lazy=True))
    courses = db.relationship('Course', secondary='track_courses', backref=db.backref('tracks', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'objectives': self.objectives,
            'outcomes': self.outcomes,
            'teacher_id': self.teacher_id,
            'courses': [course.to_dict() for course in self.courses],
            'downloadable_files': self.downloadable_files,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
