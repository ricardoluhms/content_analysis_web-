from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from caw_app.models import User
from werkzeug.utils import secure_filename

allowed_images = { 'png', 'jpg', 'jpeg', 'gif'}


class UploadImageForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),FileAllowed(allowed_images, 'Images only!')])
    submit = SubmitField('Add/Update Image')

class NameForm(FlaskForm):
    btn_style={'class': 'btn btn-success'}
    placeholder={'placeholder': 'My full name is','style': 'max-width: 100%'}
    fullname = StringField('Full Name', validators=[DataRequired()], render_kw=placeholder)
    submit = SubmitField('Add/Update')

class SimpleEmailForm(FlaskForm):
    placeholder={'placeholder':  'mail@example.com','style': 'max-width: 100%'}
    style={'class': 'btn btn-success'}
    email = StringField('Email', validators=[DataRequired()], render_kw=placeholder)
    submit = SubmitField('Change')
