from .db import db, environment, SCHEMA
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import os
import binascii
from app.utils.email_utils import send_email

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), default='Creator', nullable=False)
    _status = db.Column("status", db.String(50), default='Pre-Apply', nullable=False)
    stripe_customer_id = db.Column(db.String(120), unique=True)
    stripe_subscription_id = db.Column(db.String(120), unique=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship to Company
    company = db.relationship('Company', backref='user', uselist=False, lazy=True)
    # Add relationship to Creator
    creator = db.relationship('Creator', backref='user', uselist=False, lazy=True)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.salt = binascii.hexlify(os.urandom(16)).decode()  # Generate a new salt
        self.hashed_password = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password + self.salt)

    def is_company(self):
        return self.type == 'Company'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status != self._status:
            self.send_status_change_email(new_status, self._status)
            self._status = new_status

    def send_status_change_email(self, new_status, old_status):
        if new_status == 'Applied':
            send_email(self.email, 'Application Received', 'Thank you for applying!')
        elif new_status == 'Accepted':
            # Check if the old status is not Premium Monthly or Premium Annual
            if old_status not in ['Premium Monthly', 'Premium Annual']:
                send_email(self.email, 'Application Accepted', 'Congratulations, your application has been accepted!')
        elif new_status == 'Denied':
            send_email(self.email, 'Application Denied', 'We regret to inform you that your application has been denied.')
        elif new_status == 'Premium Monthly':
            send_email(self.email, 'Subscription Upgraded', 'You have successfully upgraded to a Premium Monthly subscription.')
        elif new_status == 'Premium Annual':
            send_email(self.email, 'Subscription Upgraded', 'You have successfully upgraded to a Premium Annual subscription.')

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'type': self.type,
            'status': self.status,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
        }
        if self.type == 'Creator':
            data['company_id'] = self.creator.company_id if self.creator else None
        else:
            data['email'] = self.email
            data['stripe_customer_id'] = self.stripe_customer_id
            data['stripe_subscription_id'] = self.stripe_subscription_id
        return data

    def validate_email(self):
        if self.is_company() and not self.email:
            raise ValueError("Email is required for Company users.")

    def save(self):
        self.validate_email()
        db.session.add(self)
        db.session.commit()
