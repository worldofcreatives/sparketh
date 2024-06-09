from app.models import db, Course
from datetime import datetime, timedelta

def seed_courses():
    courses = [
        {
            'title': 'Drawing 101',
            'description': 'Introduction to drawing',
            'skill_level': 'Beginner',
            'type': 'Art',
            'instructor_id': 2,
            'materials': ["Pencil", "Paper"],  # Provided as a list
            'length': timedelta(hours=1, minutes=30),  # Provided as a timedelta
            'intro_video': 'http://example.com/intro.mp4',
            'tips': 'Start with light strokes',
            'terms': 'No plagiarism',
            'files': {}
        }
    ]

    for course_data in courses:
        existing_course = Course.query.filter_by(title=course_data['title']).first()
        if not existing_course:
            course = Course(**course_data)
            db.session.add(course)
    db.session.commit()

def undo_courses():
    db.session.execute('TRUNCATE TABLE courses RESTART IDENTITY CASCADE;')
    db.session.commit()
