from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
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

class Problem_Space_Form(FlaskForm):
    problem_space_text =TextAreaField('Problem Space Text ', validators=[DataRequired()])
    submit8 = SubmitField('Confirm/Replace')

class Solution_Space_Form(FlaskForm):
    solution_space_text =TextAreaField('Solution Space Text ', validators=[DataRequired()])
    submit9 = SubmitField('Confirm/Replace')

class Total_Group_Form(FlaskForm):
    tt_groups =SelectField('Select number of groups: ', choices=[],coerce=int)
    submit10 = SubmitField('Confirm')

class Add_Group_Form_A(FlaskForm):
    group_name1=StringField('Group Name 1: ', validators=[DataRequired()])
    submit11 = SubmitField('Confirm')

class Add_Group_Form_B(FlaskForm):
    group_name2=StringField('Group Name 2:', validators=[DataRequired()])
    submit12 = SubmitField('Confirm/Replace')

class Add_Group_Form_C(FlaskForm):
    group_name3=StringField('Group Nname 3', validators=[DataRequired()])
    submit13 = SubmitField('Confirm/Replace')

class Add_Group_Form_D(FlaskForm):
    group_name4=StringField('Group Nname 4', validators=[DataRequired()])
    submit14 = SubmitField('Confirm/Replace')

class Add_Group_Relationship_Form(FlaskForm):
    group_name=StringField('TO BE DEFINED', validators=[DataRequired()])
    submit15 = SubmitField('Confirm')