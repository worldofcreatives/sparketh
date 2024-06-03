from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from flask_wtf.file import FileAllowed
from wtforms.widgets import ListWidget, CheckboxInput

class ProfileForm(FlaskForm):
    # Shared fields
    bio = TextAreaField('Bio', validators=[Optional()])

    # Creator-specific fields
    profile_pic = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!'),
        Optional()
    ])
    first_name = StringField('First Name', validators=[Optional(), Length(max=255)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=255)])
    stage_name = StringField('Stage Name', validators=[Optional(), Length(max=255)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address_1 = StringField('Address 1', validators=[Optional(), Length(max=255)])
    address_2 = StringField('Address 2', validators=[Optional(), Length(max=255)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[Optional(), Length(max=20)])
    portfolio_url = StringField('Portfolio URL', validators=[Optional(), Length(max=255)])
    previous_projects = TextAreaField('Previous Projects', validators=[Optional()])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=255)])
    twitter = StringField('Twitter', validators=[Optional(), Length(max=255)])
    facebook = StringField('Facebook', validators=[Optional(), Length(max=255)])
    youtube = StringField('YouTube', validators=[Optional(), Length(max=255)])
    other_social_media = TextAreaField('Other Social Media', validators=[Optional()])
    reference_name = StringField('Reference Name', validators=[Optional(), Length(max=255)])
    reference_email = StringField('Reference Email', validators=[Email(), Optional(), Length(max=255)])
    reference_phone = StringField('Reference Phone', validators=[Optional(), Length(max=20)])
    reference_relationship = StringField('Reference Relationship', validators=[Optional(), Length(max=100)])

    # Company-specific fields
    logo = FileField('Company Logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!'),
        Optional()
    ])
    name = StringField('Name', validators=[Optional(), Length(max=255)])


    def __init__(self, *args, type=None, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Adjusting form fields based on user type
        if type == 'Creator':
            del self.logo
            del self.name

        elif type == 'Company':
            del self.profile_pic
            del self.genres
            del self.types
            del self.phone
            del self.address_1
            del self.address_2
            del self.city
            del self.state
            del self.postal_code
            del self.portfolio_url
            del self.previous_projects
            del self.instagram
            del self.twitter
            del self.facebook
            del self.youtube
            del self.other_social_media
            del self.reference_name
            del self.reference_email
            del self.reference_phone
            del self.reference_relationship
            del self.stage_name
