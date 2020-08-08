from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_required
from caw_app.manage_reviews import manage_reviews_bp
from caw_app.models import Projects, Reviews, User, Wmi
from caw_app.manage_reviews.forms import New_Project_Form
from caw_app import db

@manage_reviews_bp.route('/manage_screen', methods=['GET', 'POST'])
def manage_screen():
    wmi=Wmi(current_user);  username=wmi.get_username()
    return render_template('mngt/manage_screen.html', username=username)

@manage_reviews_bp.route('/new_review', methods=['GET', 'POST'])
#@login_required
def new_review():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    form = New_Project_Form()
    
    user=User.query.filter_by(id=user_id).first()
    project_list=Projects.query.filter_by(user_id=user_id)
    if form.validate_on_submit():
        existing_project= Projects.query.filter_by(project_name=form.project_name.data).first()
        if existing_project is None:
            project = Projects(project_name=form.project_name.data, user_id=user_id)
            db.session.add(project)
            db.session.commit()
            flash('Project Name "'+form.project_name.data +'" added!')
        else:
            flash('A project already exists with that name.')
    if project_list:
        return render_template('mngt/new_review.html', form=form, project_list=project_list, username=username)
    return render_template('mngt/new_review.html', form=form, username=username)

@manage_reviews_bp.route('/')
def load_review():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### to be defined
    return render_template('mngt/load_review.html', username=username)

@manage_reviews_bp.route('/')
def share_review():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### to be defined
    return render_template('mngt/share_review.html', username=username)

""" Code example
# @products_bp.route('/view/<int:product_id>')
# def view(product_id):
#     product = Product.query.get(product_id)
#     return render_template('products/view.html', product=product) """