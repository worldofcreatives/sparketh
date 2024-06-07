from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from app.models import User

def user_exists(form, field):
    # Checking if user exists
    identifier = field.data
    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
    if not user:
        raise ValidationError('User not found.')

def password_matches(form, field):
    # Checking if password matches
    password = field.data
    identifier = form.data['identifier']
    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
    if not user:
        raise ValidationError('No such user exists.')
    if not user.check_password(password):
        raise ValidationError('Password was incorrect.')

class LoginForm(FlaskForm):
    identifier = StringField('identifier', validators=[DataRequired(), user_exists])
    password = StringField('password', validators=[DataRequired(), password_matches])
