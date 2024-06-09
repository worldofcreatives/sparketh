from .db import db, environment, SCHEMA
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    skill_level = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    materials = db.Column(db.JSON, nullable=True)
    length = db.Column(db.Interval, nullable=False)
    intro_video = db.Column(db.String(255), nullable=False)
    tips = db.Column(db.Text, nullable=True)
    terms = db.Column(db.Text, nullable=True)
    files = db.Column(db.JSON, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'skill_level': self.skill_level,
            'type': self.type,
            'instructor_id': self.instructor_id,
            'materials': self.materials,
            'length': str(self.length),
            'intro_video': self.intro_video,
            'tips': self.tips,
            'terms': self.terms,
            'files': self.files,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
