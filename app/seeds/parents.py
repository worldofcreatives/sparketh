from app.models import db, Parent, environment, SCHEMA
from sqlalchemy.sql import text

def seed_parents():
    # Example parents
    parents = [
        {
            'user_id': 1,
            'name': 'Demo Corp',
            'bio': 'A demo parent for demonstration purposes.',
            'logo': 'path/to/demo/logo.png',
        },
        {
            'user_id': 5,
            'name': 'Tech Innovations',
            'bio': 'Innovating the future of technology.',
            'logo': 'path/to/tech/innovations/logo.png',
        }
    ]

    for parent_data in parents:
        existing_parent = Parent.query.filter_by(user_id=parent_data['user_id']).first()
        if not existing_parent:
            parent = Parent(
                user_id=parent_data['user_id'],
                name=parent_data['name'],
                bio=parent_data['bio'],
                logo=parent_data['logo']
            )
            db.session.add(parent)

    db.session.commit()

def undo_parents():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.parents RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM parents"))

    db.session.commit()
