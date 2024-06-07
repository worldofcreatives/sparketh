from app.models import db, User, Parent, Student, environment, SCHEMA
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
import os
import binascii

def seed_users():
    users = [
        {
            'username': 'Demo',
            'email': 'demo@aa.io',
            'password': 'password',
            'type': 'Parent',
            'status': 'Accepted'
        },
        {
            'username': 'marnie',
            'email': 'marnie@aa.io',
            'password': 'password',
            'type': 'Student',
            'status': 'Pre-Apply',
            'parent_id': 1
        },
        {
            'username': 'bobbie',
            'email': 'bobbie@aa.io',
            'password': 'password',
            'type': 'Student',
            'status': 'Pre-Apply',
            'parent_id': 1
        },
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'password',
            'type': 'Parent',
            'status': 'Pre-Apply'
        },
        {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'password',
            'type': 'Parent',
            'status': 'Pre-Apply'
        },
        {
            'username': 'dana',
            'email': 'dana@example.com',
            'password': 'password',
            'type': 'Student',
            'status': 'Pre-Apply',
            'parent_id': 4
        },
        {
            'username': 'evan',
            'email': 'evan@example.com',
            'password': 'password',
            'type': 'Parent',
            'status': 'Pre-Apply'
        },
        {
            'username': 'fiona',
            'email': 'fiona@example.com',
            'password': 'password',
            'type': 'Student',
            'status': 'Pre-Apply',
            'parent_id': 7
        }
    ]

    for user_data in users:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            salt = binascii.hexlify(os.urandom(16)).decode()
            hashed_password = generate_password_hash(user_data['password'] + salt)
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                hashed_password=hashed_password,
                salt=salt,
                type=user_data['type'],
                status=user_data['status']
            )
            user.save()  # Using the save method to validate and commit

            if user.type == 'Parent':
                parent = Parent(user_id=user.id, name=user.username)
                db.session.add(parent)
                db.session.commit()

            elif user.type == 'Student':
                student = Student(user_id=user.id, parent_id=user_data.get('parent_id'))
                db.session.add(student)
                db.session.commit()

def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
