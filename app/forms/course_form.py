from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectMultipleField, FieldList
from wtforms.validators import DataRequired, Optional
from app.models import Type, Subject

class CourseForm(FlaskForm):
    title = StringField('title', validators=[Optional()])
    description = TextAreaField('description', validators=[Optional()])
    skill_level = StringField('skill_level', validators=[Optional()])
    type = StringField('type', validators=[Optional()])
    instructor_id = IntegerField('instructor_id', validators=[Optional()])
    materials = FieldList(StringField('Material'))
    length = StringField('length', validators=[Optional()])
    intro_video = StringField('intro_video', validators=[Optional()])
    tips = TextAreaField('tips', validators=[Optional()])
    terms = TextAreaField('terms', validators=[Optional()])
    files = FieldList(StringField('File URL'))
    types = SelectMultipleField('types', coerce=int, validators=[Optional()])  # Assuming this is a list of type IDs
    subjects = SelectMultipleField('subjects', coerce=int, validators=[Optional()])  # Assuming this is a list of subject IDs

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.types.choices = [(type_.id, type_.name) for type_ in Type.query.all()]
        self.subjects.choices = [(subject.id, subject.name) for subject in Subject.query.all()]
