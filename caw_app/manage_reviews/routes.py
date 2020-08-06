from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_required
from caw_app.manage_reviews import manage_reviews_bp
from caw_app.models import Projects, Reviews, User
from caw_app.manage_reviews.forms import New_Project_Form
from caw_app import db

@manage_reviews_bp.route('/manage_screen', methods=['GET', 'POST'])
def manage_screen():
    ### to be defined
    return render_template('mngt/manage_screen.html')

@manage_reviews_bp.route('/new_review', methods=['GET', 'POST'])
#@login_required
def new_review():
    form = New_Project_Form()
    id_num=current_user.id
    user=User.query.filter_by(id=id_num).first()
    #flash(User.query.all()); flash(user); flash(type(user.username))
    #flash(user.username); flash(id_num)
    project_list=Projects.query.filter_by(user_id=id_num)
    if form.validate_on_submit():
        existing_project= Projects.query.filter_by(project_name=form.project_name.data).first()
        if existing_project is None:
            project = Projects(project_name=form.project_name.data, user_id=id_num)
            db.session.add(project)
            db.session.commit()
            flash('Project Name "'+form.project_name.data +'" added!')
        else:
            flash('A project already exists with that name.')

    if project_list:
        return render_template('mngt/new_review.html', form=form, project_list=project_list, username=user.username)
    
    return render_template('mngt/new_review.html', form=form, username=user.username)

@manage_reviews_bp.route('/')
def load_review():
    ### to be defined
    return render_template('mngt/load_review.html')

@manage_reviews_bp.route('/')
def share_review():
    ### to be defined
    return render_template('mngt/share_review.html')

""" Code example
# @products_bp.route('/view/<int:product_id>')
# def view(product_id):
#     product = Product.query.get(product_id)
#     return render_template('products/view.html', product=product) """