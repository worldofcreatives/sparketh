# models/community_post_like.py
from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class CommunityPostLike(db.Model):
    __tablename__ = 'community_post_likes'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    post_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('community_posts.id')), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    post = db.relationship('CommunityPost', backref=db.backref('post_likes', lazy=True))
    user = db.relationship('User', backref=db.backref('community_post_likes', lazy=True))

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'created_date': self.created_date.isoformat()
        }
