# art_seeder.py

from app.models import db, Art

def seed_art():
    artworks = [
        {
            'name': 'Sunset Drawing',
            'type': 'portfolio',
            'user_id': 3,
            'course_id': 1,
            'media_url': 'http://example.com/art/sunset.jpg'
        },
        {
            'name': 'Mountain Painting',
            'type': 'portfolio',
            'user_id': 3,
            'course_id': 1,
            'media_url': 'http://example.com/art/mountain.jpg'
        }
    ]

    for art_data in artworks:
        existing_art = Art.query.filter_by(name=art_data['name']).first()
        if not existing_art:
            art = Art(**art_data)
            db.session.add(art)
    db.session.commit()

def undo_art():
    db.session.execute('TRUNCATE TABLE art RESTART IDENTITY CASCADE;')
    db.session.commit()
