from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Optional

class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=50)])
    skill_level = StringField('Skill Level', validators=[DataRequired(), Length(max=20)])
    type = StringField('Type', validators=[DataRequired(), Length(max=20)])
    instructor_id = IntegerField('Instructor ID', validators=[DataRequired()])
    materials = TextAreaField('Materials', validators=[Optional()])
    length = StringField('Length', validators=[DataRequired()])
    intro_video = StringField('Intro Video', validators=[DataRequired(), Length(max=255)])
    tips = TextAreaField('Tips', validators=[Optional()])
    terms = TextAreaField('Terms', validators=[Optional()])
    files = TextAreaField('Files', validators=[Optional()])
