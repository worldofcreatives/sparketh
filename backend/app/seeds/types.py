from app.models import db, Type, environment, SCHEMA
from sqlalchemy.sql import text

def seed_types():
    types = ['Activity', 'Challenge', 'Creative', 'Project', 'Technical']

    for type_name in types:
        existing_type = db.session.query(Type).filter_by(name=type_name).first()
        if not existing_type:
            new_type = Type(name=type_name)
            db.session.add(new_type)
    db.session.commit()

def undo_types():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.types RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("TRUNCATE types RESTART IDENTITY CASCADE;"))

    db.session.commit()
