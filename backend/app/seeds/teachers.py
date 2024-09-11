from app.models import db, Teacher

def seed_teachers():
    teachers = [
        {
            'user_id': 2,
            'profile_pic': 'path/to/profile_pic.jpg',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'address_1': '456 Elm St',
            'address_2': '',
            'city': 'Columbus',
            'state': 'OH',
            'zip_code': '43085',
            'bio': 'Experienced art teacher.',
            'expertise': 'Drawing and Painting'
        }
    ]

    for teacher_data in teachers:
        existing_teacher = Teacher.query.filter_by(user_id=teacher_data['user_id']).first()
        if not existing_teacher:
            teacher = Teacher(**teacher_data)
            db.session.add(teacher)
    db.session.commit()

def undo_teachers():
    db.session.execute('TRUNCATE TABLE teachers RESTART IDENTITY CASCADE;')
    db.session.commit()
