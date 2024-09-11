from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed

class ArtForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])  # gallery, course, and/or portfolio
    user_id = IntegerField('user_id', validators=[DataRequired()])
    course_id = IntegerField('course_id', validators=[Optional()])
    file = FileField('Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!'),
        Optional()
    ])
    public = BooleanField('public', default=True)
    open_to_feedback = BooleanField('open_to_feedback', default=False)
