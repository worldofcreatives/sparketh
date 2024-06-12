# models/user_follow.py
from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class UserFollow(db.Model):
    __tablename__ = 'user_follows'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    follower_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True)
    followee_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('following', lazy='dynamic'))
    followee = db.relationship('User', foreign_keys=[followee_id], backref=db.backref('followers', lazy='dynamic'))
