# models/poll_option.py
from .db import db, environment, SCHEMA, add_prefix_for_prod

class PollOption(db.Model):
    __tablename__ = 'poll_options'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('community_posts.id')), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'text': self.text,
            'votes': self.votes
        }
