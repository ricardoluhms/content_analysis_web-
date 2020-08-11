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

class New_Review_Form(FlaskForm):
    new_review_name =StringField('Modify Review Name', validators=[DataRequired()], )
    submit = SubmitField('Save')