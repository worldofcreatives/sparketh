from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from app.models import User
from flask_wtf.file import FileAllowed

def user_exists(form, field):
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')

class TeacherSignUpForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=40, message="Username must be between 3 and 40 characters.")
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email(message="Invalid email address."),
        user_exists
    ])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters.")
    ])
    profile_pic = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!'),
        Optional()
    ])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    address_1 = StringField('Address 1', validators=[DataRequired(), Length(max=100)])
    address_2 = StringField('Address 2', validators=[Optional(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    state = StringField('State', validators=[DataRequired(), Length(max=50)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=20)])
    bio = TextAreaField('Bio', validators=[Optional()])
    expertise = TextAreaField('Expertise', validators=[Optional()])
