from app.models import db, User, Company, Creator, environment, SCHEMA
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
            'type': 'Company',
            'status': 'Accepted'
        },
        {
            'username': 'marnie',
            'email': 'marnie@aa.io',
            'password': 'password',
            'type': 'Creator',
            'status': 'Pre-Apply',
            'company_id': 1
        },
        {
            'username': 'bobbie',
            'email': 'bobbie@aa.io',
            'password': 'password',
            'type': 'Creator',
            'status': 'Pre-Apply',
            'company_id': 1
        },
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'password',
            'type': 'Company',
            'status': 'Pre-Apply'
        },
        {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'password',
            'type': 'Company',
            'status': 'Pre-Apply'
        },
        {
            'username': 'dana',
            'email': 'dana@example.com',
            'password': 'password',
            'type': 'Creator',
            'status': 'Pre-Apply',
            'company_id': 4
        },
        {
            'username': 'evan',
            'email': 'evan@example.com',
            'password': 'password',
            'type': 'Company',
            'status': 'Pre-Apply'
        },
        {
            'username': 'fiona',
            'email': 'fiona@example.com',
            'password': 'password',
            'type': 'Creator',
            'status': 'Pre-Apply',
            'company_id': 7
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

            if user.type == 'Company':
                company = Company(user_id=user.id, name=user.username)
                db.session.add(company)
                db.session.commit()

            elif user.type == 'Creator':
                creator = Creator(user_id=user.id, company_id=user_data.get('company_id'))
                db.session.add(creator)
                db.session.commit()

def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()


# from app.models import db, User, environment, SCHEMA
# from werkzeug.security import generate_password_hash
# from sqlalchemy.sql import text
# import os
# import binascii

# def seed_users():
#     users = [
#         {
#             'username': 'Demo',
#             'email': 'demo@aa.io',
#             'password': 'password',
#             'type': 'Company',
#             'status': 'Accepted'
#         },
#         {
#             'username': 'marnie',
#             'email': 'marnie@aa.io',
#             'password': 'password',
#             'type': 'Creator',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'bobbie',
#             'email': 'bobbie@aa.io',
#             'password': 'password',
#             'type': 'Creator',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'alice',
#             'email': 'alice@example.com',
#             'password': 'password',
#             'type': 'Company',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'charlie',
#             'email': 'charlie@example.com',
#             'password': 'password',
#             'type': 'Company',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'dana',
#             'email': 'dana@example.com',
#             'password': 'password',
#             'type': 'Creator',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'evan',
#             'email': 'evan@example.com',
#             'password': 'password',
#             'type': 'Company',
#             'status': 'Pre-Apply'
#         },
#         {
#             'username': 'fiona',
#             'email': 'fiona@example.com',
#             'password': 'password',
#             'type': 'Creator',
#             'status': 'Pre-Apply'
#         }
#     ]

#     for user_data in users:
#         existing_user = User.query.filter_by(email=user_data['email']).first()
#         if not existing_user:
#             salt = binascii.hexlify(os.urandom(16)).decode()
#             hashed_password = generate_password_hash(user_data['password'] + salt)
#             user = User(
#                 username=user_data['username'],
#                 email=user_data['email'],
#                 hashed_password=hashed_password,
#                 salt=salt,
#                 type=user_data['type'],
#                 status=user_data['status']
#             )
#             db.session.add(user)

#     db.session.commit()

# def undo_users():
#     if environment == "production":
#         db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
#     else:
#         db.session.execute(text("DELETE FROM users"))

#     db.session.commit()
