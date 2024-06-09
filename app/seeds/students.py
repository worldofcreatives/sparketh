from app.models import db, Student, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import date, datetime

def seed_students():
    # Example students
    students = [
        {
            'user_id': 2,
            'parent_id': 1,
            'profile_pic': 'url/profile.png',
            'bio': 'Exploring creativity in every aspect.',
            'date_of_birth': date(2010, 1, 1),
            'skill_level': 'Beginner',
            'progress': {},
            'created_date': datetime.utcnow(),
            'updated_date': datetime.utcnow(),
        },
        {
            'user_id': 3,
            'parent_id': 1,
            'profile_pic': 'url/profile.png',
            'bio': 'Innovating art for the new age.',
            'date_of_birth': date(2008, 5, 20),
            'skill_level': 'Intermediate',
            'progress': {},
            'created_date': datetime.utcnow(),
            'updated_date': datetime.utcnow(),
        },
        # Add more students as needed
    ]

    for student_data in students:
        existing_student = Student.query.filter_by(user_id=student_data['user_id']).first()
        if not existing_student:
            student = Student(
                user_id=student_data['user_id'],
                parent_id=student_data['parent_id'],
                profile_pic=student_data['profile_pic'],
                bio=student_data['bio'],
                date_of_birth=student_data['date_of_birth'],
                skill_level=student_data['skill_level'],
                progress=student_data['progress'],
                created_date=student_data['created_date'],
                updated_date=student_data['updated_date']
            )
            db.session.add(student)

    db.session.commit()

def undo_students():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.students RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM students"))

    db.session.commit()
