from .db import db, environment, SCHEMA
from datetime import datetime

# Association table for Child and Types
child_type_table = db.Table('child_types',
    db.Column('child_id', db.Integer, db.ForeignKey('children.id'), primary_key=True),
    db.Column('type_id', db.Integer, db.ForeignKey('types.id'), primary_key=True)
)

# Association table for Child and Subjects
child_subject_table = db.Table('child_subjects',
    db.Column('child_id', db.Integer, db.ForeignKey('children.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

class Child(db.Model):
    __tablename__ = 'children'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    skill_level = db.Column(db.String(20), nullable=True)
    progress = db.Column(db.JSON, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    types = db.relationship('Type', secondary=child_type_table, backref=db.backref('children', lazy=True))
    subjects = db.relationship('Subject', secondary=child_subject_table, backref=db.backref('children', lazy=True))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'date_of_birth': self.date_of_birth.isoformat(),
            'skill_level': self.skill_level,
            'progress': self.progress,
            'parent_id': self.parent_id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'types': [type_.to_dict() for type_ in self.types],
            'subjects': [subject.to_dict() for subject in self.subjects]
        }
