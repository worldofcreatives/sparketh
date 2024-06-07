from app.models import db, Student, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_students():
    # Example students
    students = [
        {
            'user_id': 2,
            'first_name': None,
            'last_name': None,
            'stage_name': None,
            'profile_pic': 'url/profile.png',
            'bio': 'Exploring creativity in every aspect.',
            'phone': None,
            'address_1': None,
            'address_2': None,
            'city': None,
            'state': None,
            'postal_code': None,
            'portfolio_url': None,
            'previous_projects': None,
            'instagram': None,
            'twitter': None,
            'facebook': None,
            'youtube': None,
            'other_social_media': None,
            'reference_name': None,
            'reference_email': None,
            'reference_phone': None,
            'reference_relationship': None,
            'created_date': datetime.utcnow(),
            'updated_date': datetime.utcnow(),
        },
        {
            'user_id': 3,
            'first_name': None,
            'last_name': None,
            'stage_name': None,
            'profile_pic': 'url/profile.png',
            'bio': 'Innovating art for the new age.',
            'phone': None,
            'address_1': None,
            'address_2': None,
            'city': None,
            'state': None,
            'postal_code': None,
            'portfolio_url': None,
            'previous_projects': None,
            'instagram': None,
            'twitter': None,
            'facebook': None,
            'youtube': None,
            'other_social_media': None,
            'reference_name': None,
            'reference_email': None,
            'reference_phone': None,
            'reference_relationship': None,
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
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                stage_name=student_data['stage_name'],
                profile_pic=student_data['profile_pic'],
                bio=student_data['bio'],
                phone=student_data['phone'],
                address_1=student_data['address_1'],
                address_2=student_data['address_2'],
                city=student_data['city'],
                state=student_data['state'],
                postal_code=student_data['postal_code'],
                portfolio_url=student_data['portfolio_url'],
                previous_projects=student_data['previous_projects'],
                instagram=student_data['instagram'],
                twitter=student_data['twitter'],
                facebook=student_data['facebook'],
                youtube=student_data['youtube'],
                other_social_media=student_data['other_social_media'],
                reference_name=student_data['reference_name'],
                reference_email=student_data['reference_email'],
                reference_phone=student_data['reference_phone'],
                reference_relationship=student_data['reference_relationship'],
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
