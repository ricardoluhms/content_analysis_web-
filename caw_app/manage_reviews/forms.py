from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from caw_app.models import User, Projects, Reviews

class New_Project_Form(FlaskForm):
    style={'class': 'btn btn-success'}
    #style2={'class': 'btn btn-success'}
    project_name = StringField('Project Name', validators=[DataRequired()], )
    submit = SubmitField('Save',render_kw=style)