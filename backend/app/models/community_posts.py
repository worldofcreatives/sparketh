# models/community_post.py
from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class CommunityPost(db.Model):
    __tablename__ = 'community_posts'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    post_type = db.Column(db.String(20), nullable=False)  # 'share_art', 'question', 'poll'
    text = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    hidden = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User', backref=db.backref('community_posts', lazy=True))
    poll_options = db.relationship('PollOption', backref='community_post', lazy=True)
    likes = db.relationship('CommunityPostLike', backref='community_post', lazy=True)
    comments = db.relationship('CommunityComment', backref='community_post', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_type': self.post_type,
            'text': self.text,
            'image_url': self.image_url,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'hidden': self.hidden,
            'poll_options': [option.to_dict() for option in self.poll_options],
            'likes': [like.user_id for like in self.likes],
            'comments': [comment.to_dict() for comment in self.comments]
        }
