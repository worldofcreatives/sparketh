from app.models import db, Opportunity, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_opportunities():
    opportunity1 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Music for Commercial',
        description='Seeking original music to feature in a national commercial.',
        target_audience='All Ages',
        budget=5000.00,
        guidelines='Original music only, any genre.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity2 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Theme Song for Podcast',
        description='Looking for a catchy theme song for our new tech podcast.',
        target_audience='Tech Enthusiasts',
        budget=2000.00,
        guidelines='Must be catchy and no longer than 30 seconds.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity3 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Artwork for Digital Game',
        description='Seeking captivating artwork to integrate into our upcoming digital game.',
        target_audience='Gamers',
        budget=7000.00,
        guidelines='High-resolution digital art, fantasy themes preferred.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity4 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Copywriter for Ad Campaign',
        description='In need of a creative copywriter for our new ad campaign.',
        target_audience='Young Adults',
        budget=3000.00,
        guidelines='Engaging and persuasive text, experience with social media a plus.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity5 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Chef for Culinary Workshop',
        description='Looking for a chef to lead a series of culinary workshops.',
        target_audience='Food Enthusiasts',
        budget=1500.00,
        guidelines='Specializes in Italian cuisine, hands-on teaching experience required.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity6 = Opportunity(
        parent_id=1,
        user_id=1,
        name='Developer for Mobile App',
        description='Seeking a skilled developer to create a mobile application for our startup.',
        target_audience='General Public',
        budget=10000.00,
        guidelines='Experience with iOS and Android, portfolio required.',
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity7 = Opportunity(
        parent_id=1,
        user_id=1,
        name="Illustrator for Children's Book",
        description="Looking for an illustrator to bring to life a series of children's books.",
        target_audience="Children",
        budget=4000.00,
        guidelines="Colorful, engaging illustrations that appeal to children aged 4-8.",
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity8 = Opportunity(
        parent_id=1,
        user_id=1,
        name="Photographer for Event",
        description="In need of a professional photographer for a corporate event.",
        target_audience="Corporate",
        budget=2500.00,
        guidelines="Must have experience with event photography, portfolio required.",
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity9 = Opportunity(
        parent_id=1,
        user_id=1,
        name="Social Media Manager",
        description="Seeking a social media manager to increase our brand's online presence.",
        target_audience="General Public",
        budget=3500.00,
        guidelines="Proven track record of growing social media accounts, creative content creation.",
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    opportunity10 = Opportunity(
        parent_id=1,
        user_id=1,
        name="Voice Actor for Animated Series",
        description="Looking for talented voice actors for our new animated series.",
        target_audience="Teens and Young Adults",
        budget=8000.00,
        guidelines="Dynamic range and ability to portray multiple characters.",
        created_date=datetime.now(),
        updated_date=datetime.now()
    )

    db.session.add_all([opportunity1, opportunity2, opportunity3, opportunity4, opportunity5, opportunity6, opportunity7, opportunity8, opportunity9, opportunity10])

    db.session.commit()

def undo_opportunities():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.opportunities RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM opportunities"))

    db.session.commit()
