from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from sqlalchemy import Enum

# Association table for Submissions and Genres
submission_genre_table = db.Table('submission_genres',
    db.Column('submission_id', db.Integer, db.ForeignKey('submissions.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

# Association table for Submissions and Types
submission_type_table = db.Table('submission_types',
    db.Column('submission_id', db.Integer, db.ForeignKey('submissions.id'), primary_key=True),
    db.Column('type_id', db.Integer, db.ForeignKey('types.id'), primary_key=True)
)

class Submission(db.Model):
    __tablename__ = 'submissions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('opportunities.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    username = db.Column(db.String(40), nullable=False)
    name = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    notes = db.Column(db.Text, nullable=True)
    bpm = db.Column(db.Integer, nullable=True)
    file_url = db.Column(db.String(500), nullable=True)
    collaborators = db.Column(db.String(500), nullable=True)
    genres = db.relationship('Genre', secondary=submission_genre_table, backref=db.backref('submissions', lazy=True))
    types = db.relationship('Type', secondary=submission_type_table, backref=db.backref('submissions', lazy=True))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Opportunity
    opportunity = db.relationship('Opportunity', backref=db.backref('submissions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'opportunity_id': self.opportunity_id,
            'opportunity_name': self.opportunity.name,
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
            'status': self.status,
            'notes': self.notes,
            'bpm': self.bpm,
            'file_url': self.file_url,
            'collaborators': self.collaborators,
            'genres': [genre.to_dict() for genre in self.genres],
            'types': [type_.to_dict() for type_ in self.types],
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'subMedia': [media.to_dict() for media in self.subMedia],
        }
