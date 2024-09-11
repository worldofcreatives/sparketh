from app.models import db, Parent

def seed_parents():
    parents = [
        {
            'user_id': 1,
            'profile_pic': 'path/to/profile_pic.jpg',
            'first_name': 'John',
            'last_name': 'Doe',
            'address_1': '123 Main St',
            'address_2': '',
            'city': 'Columbus',
            'state': 'OH',
            'zip_code': '43085',
            'stripe_customer_id': 'cus_123456789',
            'stripe_subscription_id': 'sub_123456789'
        }
    ]

    for parent_data in parents:
        existing_parent = Parent.query.filter_by(user_id=parent_data['user_id']).first()
        if not existing_parent:
            parent = Parent(**parent_data)
            db.session.add(parent)
    db.session.commit()

def undo_parents():
    db.session.execute('TRUNCATE TABLE parents RESTART IDENTITY CASCADE;')
    db.session.commit()
