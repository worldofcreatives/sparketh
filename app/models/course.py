# course.py

from .db import db, environment, SCHEMA
from datetime import datetime

# Association table for Courses and Types
course_type_table = db.Table('course_types',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('type_id', db.Integer, db.ForeignKey('types.id'), primary_key=True)
)

# Association table for Courses and Subjects
course_subject_table = db.Table('course_subjects',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

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
    types = db.relationship('Type', secondary=course_type_table, backref=db.backref('courses', lazy=True))
    subjects = db.relationship('Subject', secondary=course_subject_table, backref=db.backref('courses', lazy=True))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Art
    student_work = db.relationship('Art', backref='course', lazy=True)

    # def validate_types(self):
    #     if not all(type_ in VALID_TYPES for type_ in self.types):
    #         raise ValueError("One or more types are invalid")

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
            'updated_date': self.updated_date.isoformat(),
            'student_work': [art.to_dict() for art in self.student_work],
            'types': [type_.to_dict() for type_ in self.types],
            'subjects': [subject.to_dict() for subject in self.subjects]
        }
