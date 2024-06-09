from app.models import db, Lesson

def seed_lessons():
    lessons = [
        {
            'title': 'Lesson 1: Basic Shapes',
            'course_id': 1,
            'url': 'http://example.com/lesson1.mp4'
        },
        {
            'title': 'Lesson 2: Shading',
            'course_id': 1,
            'url': 'http://example.com/lesson2.mp4'
        }
    ]

    for lesson_data in lessons:
        existing_lesson = Lesson.query.filter_by(title=lesson_data['title']).first()
        if not existing_lesson:
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
    db.session.commit()

def undo_lessons():
    db.session.execute('TRUNCATE TABLE lessons RESTART IDENTITY CASCADE;')
    db.session.commit()
