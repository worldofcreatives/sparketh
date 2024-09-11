# models/community_comment.py
from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class CommunityComment(db.Model):
    __tablename__ = 'community_comments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('community_posts.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    text = db.Column(db.Text, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('community_comments.id')), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('community_comments', lazy=True))
    parent_comment = db.relationship('CommunityComment', remote_side=[id], backref='replies')

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'text': self.text,
            'parent_comment_id': self.parent_comment_id,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'replies': [reply.to_dict() for reply in self.replies]
        }
