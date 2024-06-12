# models/associations.py
from .db import db, environment, SCHEMA, add_prefix_for_prod

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

# Association table for Student and Courses (joined courses)
student_course_table = db.Table(
    'student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey(add_prefix_for_prod('students.id')), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey(add_prefix_for_prod('courses.id')), primary_key=True)
)

# Association table for Student and Lessons (completed lessons)
student_lesson_table = db.Table(
    'student_lessons',
    db.Column('student_id', db.Integer, db.ForeignKey(add_prefix_for_prod('students.id')), primary_key=True),
    db.Column('lesson_id', db.Integer, db.ForeignKey(add_prefix_for_prod('lessons.id')), primary_key=True)
)

# Association table for Track and Courses
track_course_table = db.Table(
    'track_courses',
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('order', db.Integer, nullable=False)
)

# Association table for Student and Tracks
student_track_table = db.Table(
    'student_tracks',
    db.Column('student_id', db.Integer, db.ForeignKey(add_prefix_for_prod('students.id')), primary_key=True),
    db.Column('track_id', db.Integer, db.ForeignKey(add_prefix_for_prod('tracks.id')), primary_key=True)
)

class StudentCourseProgress(db.Model):
    __tablename__ = 'student_course_progress'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    student_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('students.id')), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('courses.id')), primary_key=True)
    progress = db.Column(db.Float, nullable=False, default=0.0)
    completed = db.Column(db.Boolean, nullable=False, default=False)


# # Association table for Student and Courses (progress)
# student_course_progress_table = db.Table(
#     'student_course_progress',
#     db.Column('student_id', db.Integer, db.ForeignKey(add_prefix_for_prod('students.id')), primary_key=True),
#     db.Column('course_id', db.Integer, db.ForeignKey(add_prefix_for_prod('courses.id')), primary_key=True),
#     db.Column('progress', db.Float, nullable=False, default=0.0),
#     db.Column('completed', db.Boolean, nullable=False, default=False)
# )
