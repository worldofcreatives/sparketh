from app.models import db, Subject, environment, SCHEMA
from sqlalchemy.sql import text

def seed_subjects():
    subjects = ['Art', 'Dance', 'Music', 'Film', 'Coding']

    for subject_name in subjects:
        existing_subject = db.session.query(Subject).filter_by(name=subject_name).first()
        if not existing_subject:
            new_subject = Subject(name=subject_name)
            db.session.add(new_subject)
    db.session.commit()

def undo_subjects():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.subjects RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("TRUNCATE subjects RESTART IDENTITY CASCADE;"))

    db.session.commit()
