from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

def username_exists(form, field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')

class StudentSignUpForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=40, message="Username must be between 3 and 40 characters."),
        username_exists
    ])
    password = StringField('password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters."),
    ])
