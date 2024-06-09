from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

def username_exists(form, field):
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')

class StudentSignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40), username_exists])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
