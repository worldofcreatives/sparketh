from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from app.models import Type, Subject

class CourseForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    skill_level = StringField('skill_level', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
    instructor_id = IntegerField('instructor_id', validators=[DataRequired()])
    length = StringField('length', validators=[DataRequired()])
    intro_video = StringField('intro_video', validators=[DataRequired()])
    tips = TextAreaField('tips')
    terms = TextAreaField('terms')
    types = SelectMultipleField('types', coerce=int)
    subjects = SelectMultipleField('subjects', coerce=int)

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.types.choices = [(type_.id, type_.name) for type_ in Type.query.all()]
        self.subjects.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
