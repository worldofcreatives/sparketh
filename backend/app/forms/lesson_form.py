from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

class LessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    course_id = IntegerField('Course ID', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), Length(max=255)])
