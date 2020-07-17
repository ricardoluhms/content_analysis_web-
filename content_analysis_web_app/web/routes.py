from web import app
#### Flask Modules
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user
#### Login Modules
from web.login import LoginForm
#### Backend Web Modules
#from analysis.text_analysisV2 import CSVs_to_Excel

#### Routes
#### ## Index
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('base.html',title="index", code='not_user')

#### ## User Page
@app.route('/users/<name>')
def user(name):
    user={'username':name}
    return render_template('user.html', user=user, name=name, code='is_user')

#### ## Questionnaires PAge
@app.route('/users/<name>/questionnaire')
def question(name):
    user={'username':name}
    return render_template('question.html', user=user, name=name, code='is_user')

### ## Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
                        form.username.data, form.remember_me.data))
    return render_template('login.html', title= "Sign in", form=form, code='not_user')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('login'))
#         #return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
