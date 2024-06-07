from .db import db
from .db import environment, SCHEMA, add_prefix_for_prod

# Associations

opp_media_table = db.Table('opp_media',
    db.Column('opportunities_id', db.Integer, db.ForeignKey(add_prefix_for_prod('opportunities.id')), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey(add_prefix_for_prod('media.id')), primary_key=True)
)
if environment == "production":
       opp_media_table.schema = SCHEMA

sub_media_table = db.Table('sub_media',
    db.Column('submissions_id', db.Integer, db.ForeignKey(add_prefix_for_prod('submissions.id')), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey(add_prefix_for_prod('media.id')), primary_key=True)
)
if environment == "production":
       sub_media_table.schema = SCHEMA

feedback_media_table = db.Table('feedback_media',
    db.Column('feedback_id', db.Integer, db.ForeignKey(add_prefix_for_prod('feedback.id')), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey(add_prefix_for_prod('media.id')), primary_key=True)
)
if environment == "production":
       feedback_media_table.schema = SCHEMA


# Models
from .user import User
from .student import Student
from .parent import Parent
from .opportunity import Opportunity
from .media import Media
from .submission import Submission
from .feedback import Feedback
from .genre import Genre
from .type import Type
