from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

# Association table for Student and Types
student_type_table = db.Table('student_types',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('type_id', db.Integer, db.ForeignKey('types.id'), primary_key=True)
)

# Association table for Student and Subjects
student_subject_table = db.Table('student_subjects',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__ = 'students'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('parents.id')), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    skill_level = db.Column(db.String(20), nullable=True)
    progress = db.Column(db.JSON, nullable=True)
    types = db.relationship('Type', secondary=student_type_table, backref=db.backref('students', lazy=True))
    subjects = db.relationship('Subject', secondary=student_subject_table, backref=db.backref('students', lazy=True))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'date_of_birth': self.date_of_birth.isoformat(),
            'skill_level': self.skill_level,
            'progress': self.progress,
            'types': [type_.to_dict() for type_ in self.types],
            'subjects': [subject.to_dict() for subject in self.subjects],
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
