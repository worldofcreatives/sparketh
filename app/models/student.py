# models/student.py
from .db import db, environment, SCHEMA
from datetime import datetime
from .associations import student_course_table, student_lesson_table, student_type_table, student_subject_table, StudentCourseProgress

class Student(db.Model):
    __tablename__ = 'students'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    skill_level = db.Column(db.String(20), nullable=True)
    points = db.Column(db.Integer, nullable=False, default=0)
    types = db.relationship('Type', secondary=student_type_table, backref=db.backref('students', lazy=True))
    subjects = db.relationship('Subject', secondary=student_subject_table, backref=db.backref('students', lazy=True))
    joined_courses = db.relationship('Course', secondary=student_course_table, backref=db.backref('students_joined', lazy=True))
    completed_lessons = db.relationship('Lesson', secondary=student_lesson_table, backref=db.backref('students_completed', lazy=True))
    course_progress = db.relationship('StudentCourseProgress', backref='student', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'skill_level': self.skill_level,
            'points': self.points,
            'types': [type_.id for type_ in self.types],  # Only include type IDs
            'subjects': [subject.id for subject in self.subjects],  # Only include subject IDs
            'joined_courses': [course.id for course in self.joined_courses],  # Only include course IDs
            'completed_lessons': [lesson.id for lesson in self.completed_lessons],  # Only include lesson IDs
            'course_progress': {cp.course_id: {'progress': cp.progress, 'completed': cp.completed} for cp in self.course_progress},
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }
