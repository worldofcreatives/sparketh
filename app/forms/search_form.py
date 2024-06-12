from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import Optional

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[Optional()])
    category = SelectField('Category', choices=[('students', 'Students'), ('parents', 'Parents'), ('opportunities', 'Opportunities')], validators=[Optional()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Search')

