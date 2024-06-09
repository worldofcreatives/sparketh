# child_seeder.py

from app.models import db, Child
from datetime import date

def seed_children():
    children = [
        {
            'user_id': 3,
            'name': 'Child One',
            'date_of_birth': date(2010, 1, 1),
            'skill_level': 'Beginner',
            'profile_pic': 'url/profile.png',
            'bio': 'Exploring creativity in every aspect.',
            'progress': '{}',
            'parent_id': 1  # Make sure this corresponds to an existing parent ID
        }
    ]

    for child_data in children:
        existing_child = Child.query.filter_by(user_id=child_data['user_id']).first()
        if not existing_child:
            child = Child(**child_data)
            db.session.add(child)
    db.session.commit()

def undo_children():
    db.session.execute('TRUNCATE TABLE children RESTART IDENTITY CASCADE;')
    db.session.commit()
