from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class ArtForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    type = StringField('Type', validators=[DataRequired(), Length(max=50)])  # gallery, course, and/or portfolio
    user_id = IntegerField('User ID', validators=[DataRequired()])
    course_id = IntegerField('Course ID', validators=[Optional()])
    media_url = StringField('Media URL', validators=[DataRequired(), Length(max=255)])
