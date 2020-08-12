from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_required
from caw_app.manage_reviews import manage_reviews_bp
from caw_app.models import Projects, Reviews, User, Wmi
from caw_app.manage_reviews.forms import New_Project_Form, Search_Project_Form, Manage_Review_Form,\
    Edit_Review_Name_Form
from caw_app import db

@manage_reviews_bp.route('/manage_screen', methods=['GET', 'POST'])
def manage_screen():
    wmi=Wmi(current_user);  username=wmi.get_username()
    return render_template('mngt/manage_screen.html', username=username)

@manage_reviews_bp.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    form = New_Project_Form()
    form2 = Search_Project_Form()
    user=User.query.filter_by(id=user_id).first()
    project_list=Projects.query.filter_by(user_id=user_id)
    form2.project_nameB.choices= [(project.project_name,project.project_name) for project in project_list]
    if form.validate_on_submit() and form.project_nameA.data:
        existing_project= Projects.query.filter_by(project_name=form.project_nameA.data).first()
        if existing_project is None:
            project = Projects(project_name=form.project_nameA.data, user_id=user_id)
            db.session.add(project)
            db.session.commit()
            flash('Project Name "'+form.project_nameA.data +'" added!')
        else:
            flash('A project already exists with that name.')
    if form2.validate_on_submit() and form2.submit2.data:
        pjct= Projects.query.filter_by(project_name=form2.project_nameB.data).first()
        reviews=Reviews.query.filter_by(project_id=pjct.id).all()
        if reviews:
            review=Reviews.query.filter_by(project_id=pjct.id).first()
            review_name=review.review_name
        else:
            review_name=str(pjct.project_name)+":_Review_Iteration__0"
            create_new_review=Reviews(review_name=review_name, project_id=pjct.id)
            db.session.add(create_new_review)
            db.session.commit()
        return redirect(url_for("mngt.new_review",project_name=form2.project_nameB.data, review_name=review_name)) 
    elif form2.validate_on_submit() and form2.submit3.data:
        project= Projects.query.filter_by(project_name=form2.project_nameB.data, user_id=user_id).first()
        db.session.delete(project)
        db.session.commit()
        project_list=Projects.query.filter_by(user_id=user_id)
        flash('Project Name "'+form2.project_nameB.data +'" deleted!')
        return render_template('mngt/new_project.html', form=form, form2=form2, project_list=project_list, username=username)
    if project_list:
        return render_template('mngt/new_project.html', form=form, form2=form2, project_list=project_list, username=username)
    return render_template('mngt/new_project.html', form=form, form2=form2, username=username)

@manage_reviews_bp.route('/load_project')
def load_project():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### to be defined
    return render_template('mngt/load_project.html', username=username)

@manage_reviews_bp.route('/share_project')
def share_project():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### to be defined
    return render_template('mngt/share_project.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>', methods=['GET', 'POST'])
@login_required
def new_review(project_name,review_name):
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### Start Forms
    form1=Edit_Review_Name_Form()
    form2=Manage_Review_Form()
    
    ### Load data from DB
    project=Projects.query.filter_by(project_name=project_name).first()
    current_review=Reviews.query.filter_by(review_name=review_name, project_id=project.id).first()

    reviews=Reviews.query.filter_by(project_id=project.id).all()
    form2.review_names.choices= [(revy.review_name,revy.review_name) for revy in reviews]

    
    ###Modifiy review name form
    if form1.validate_on_submit() and form1.submit4.data:
        if not current_review:
            current_review=Reviews.query.filter_by(project_id=project.id).first()
        review_name=form1.new_review_name.data+"_Iteration__0"
        current_review.review_name=review_name
        db.session.add(current_review)
        db.session.commit()
        return redirect(url_for("mngt.new_review",
                                project_name=project_name, 
                                review_name=review_name)
                       )

    ###Open review 
    if form2.validate_on_submit() and form2.submit5.data:
        review_name=form2.review_names.data
        return redirect(url_for("mngt.solution_problem_space",
                                project_name=project_name, 
                                review_name=review_name)
                        )
    ###Delete review name form
    elif form2.validate_on_submit() and form2.submit6.data:
        selected_review= Reviews.query.filter_by(project_id=project.id, review_name=form2.review_names.data).first()
        db.session.delete(selected_review)
        db.session.commit()
        review=Reviews.query.filter_by(project_id=project.id).first()
        review_name=review.review_name
        
        return redirect(url_for("mngt.new_review",
                                project_name=project_name, 
                                review_name=review_name)
                        )

    #Add New Review Itereration
    elif form2.validate_on_submit() and form2.submit7.data:
        selected_review= Reviews.query.filter_by(project_id=project.id, review_name=form2.review_names.data).first()
        prev_iter_name=selected_review.review_name
        review_name=prev_iter_name.split('_Iteration__')[0]+'_Iteration__'+str(int(prev_iter_name.split('_Iteration__')[1])+1)
        create_new_review=Reviews(review_name=review_name, project_id=project.id)
        db.session.add(create_new_review)
        db.session.commit()
        return redirect(url_for("mngt.new_review",
                                project_name=project_name, 
                                review_name=review_name))

    return render_template('mngt/new_review.html', 
                            username=username, 
                            project_name=project_name, 
                            review_name=review_name,
                            form1=form1 , form2=form2)
    
@manage_reviews_bp.route('/<project_name>/<review_name>/solution_problem_space', methods=['GET', 'POST'])
@login_required
def solution_problem_space(project_name,review_name):
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    return render_template('mngt/solution_problem_space.html', username=username)


@manage_reviews_bp.route('/<project_name>/<review_name>/groups_space', methods=['GET', 'POST'])
def groups_space(project_name,review_name):
    ### to be defined
    return render_template('mngt/groups_space.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/group_relation', methods=['GET', 'POST'])
def group_relation(project_name,review_name):
    ### to be defined
    return render_template('mngt/group_relation.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/venn_diagram', methods=['GET', 'POST'])
def venn_diagram(project_name,review_name):
    ### to be defined
    return render_template('mngt/venn_diagram.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/group_keywords', methods=['GET', 'POST'])
def group_keywords(project_name,review_name):
    ### to be defined
    return render_template('mngt/group_keywords.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/other_features', methods=['GET', 'POST'])
def other_features(project_name,review_name):
    ### to be defined
    return render_template('mngt/other_features.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/keywords_exclusions', methods=['GET', 'POST'])
def keywords_exclusions(project_name,review_name):
    ### to be defined
    return render_template('mngt/keywords_exclusions.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/search_string', methods=['GET', 'POST'])
def search_string(project_name,review_name):
    ### to be defined
    return render_template('mngt/search_string.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/search_results', methods=['GET', 'POST'])
def search_results(project_name,review_name):
    ### to be defined
    return render_template('mngt/search_results.html', username=username)

@manage_reviews_bp.route('/<project_name>/<review_name>/analysis', methods=['GET', 'POST'])
def analysis(project_name,review_name):
    ### to be defined
    return render_template('mngt/search_results.html', username=username)
