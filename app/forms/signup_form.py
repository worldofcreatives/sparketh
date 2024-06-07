from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length, Regexp
from app.models import User

def user_exists(form, field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')

def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=40, message="Username must be between 3 and 40 characters."),
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email(message="Invalid email address."),
        user_exists
    ])
    password = StringField('password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters."),
    ])
    user_type = SelectField('User Type', choices=[('Company', 'Company'), ('Creator', 'Creator')], validators=[DataRequired()])
