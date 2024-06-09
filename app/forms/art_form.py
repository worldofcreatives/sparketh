from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired

class ArtForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])  # gallery, course, and/or portfolio
    user_id = IntegerField('user_id', validators=[DataRequired()])
    course_id = IntegerField('course_id', validators=[DataRequired()])
    file = FileField('file', validators=[DataRequired()])
