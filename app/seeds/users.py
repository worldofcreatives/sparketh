from app.models import db, User
from werkzeug.security import generate_password_hash
import os
import binascii

def seed_users():
    users = [
        {
            'username': 'parent1',
            'email': 'parent1@example.com',
            'password': 'password',
            'type': 'parent',
            'status': 'active'
        },
        {
            'username': 'teacher1',
            'email': 'teacher1@example.com',
            'password': 'password',
            'type': 'teacher',
            'status': 'active'
        },
        {
            'username': 'child1',
            'email': None,
            'password': 'password',
            'type': 'child',
            'status': 'active'
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
            db.session.add(user)
    db.session.commit()

def undo_users():
    db.session.execute('TRUNCATE TABLE users RESTART IDENTITY CASCADE;')
    db.session.commit()
