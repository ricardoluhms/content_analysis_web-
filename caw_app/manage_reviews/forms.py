from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from caw_app.models import User, Projects, Reviews

class New_Project_Form(FlaskForm):
    project_nameA = StringField('Project Name', validators=[DataRequired()], )
    submit = SubmitField('Save')

class Search_Project_Form(FlaskForm):
    project_nameB =SelectField('Project Name', choices=[])
    submit2 = SubmitField('Open')
    submit3 = SubmitField('Delete')

class Edit_Review_Name_Form(FlaskForm):
    new_review_name = StringField('Review Name')
    submit4 = SubmitField('Rename Review')

class Manage_Review_Form(FlaskForm):
    review_names =SelectField('Existing Reviews', choices=[])
    submit5 = SubmitField('Open Review')
    submit6 = SubmitField('Delete Review')
    submit7 = SubmitField('Add New Review Itereration')