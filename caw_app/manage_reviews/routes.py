from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user, login_required
from caw_app.manage_reviews import manage_reviews_bp
from caw_app.models import Projects, Reviews, User, Wmi
from caw_app.manage_reviews.forms import New_Project_Form, \
    Search_Project_Form, Manage_Review_Form,\
    Edit_Review_Name_Form,Total_Group_Form, \
    Problem_Space_Form, Solution_Space_Form, \
    Add_Group_Form_A, Add_Group_Form_B, Add_Group_Form_C, Add_Group_Form_D
from caw_app import db


class Check:
    def __init__(self,current_user):
        wmi=Wmi(current_user);
        self.user_id=wmi.get_user_id()
        self.username=wmi.get_username()
    def one_project(self,name=None):
        if name:
            self.project=Projects.query.filter_by(user_id=self.user_id, project_name=name).first()
        else:
            self.project=Projects.query.filter_by(user_id=self.user_id).first()
        return self.project

    def many_project(self):
        self.many_projects=Projects.query.filter_by(user_id=self.user_id).all()
        return self.many_projects
    
    def one_review(self,rname=None):
        if self.project:
            if rname:
                self.review=Reviews.query.filter_by(project_id=self.project.id, review_name=rname).first()
            else:
                self.review=Reviews.query.filter_by(project_id=self.project.id).first()
        else:
            self.review=None
        return self.review

    def many_review(self):
        if self.project:
            self.many_reviews=Reviews.query.filter_by(project_id=self.project.id).all()
        else:
            self.many_reviews=None
        return self.many_reviews

@manage_reviews_bp.route('/manage_screen', methods=['GET', 'POST'])
def manage_screen():
    check=Check(current_user)
    project_name=check.one_project().project_name  
    review_name=check.one_review().review_name
    if check.one_project() and check.one_review():
        return render_template("mngt/manage_screen.html",
                                username=check.username,
                                project_name=project_name, 
                                review_name=review_name)
    elif check.one_project():
        return render_template("mngt/manage_screen.html",
                                username=check.username,
                                project_name=project_name)

    return render_template('mngt/manage_screen.html',  username=check.username)

@manage_reviews_bp.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    
    check=Check(current_user)
    project_list=check.many_project()

    form = New_Project_Form()
    form2 = Search_Project_Form()

    form2.project_nameB.choices= [(project.project_name,project.project_name) for project in project_list]
    if form.validate_on_submit() and form.project_nameA.data:
        existing_project= check.one_project(form.project_nameA.data)
        if existing_project is None:
            project = Projects(project_name=form.project_nameA.data, user_id=check.id)
            db.session.add(project)
            db.session.commit()
            flash('Project Name "'+form.project_nameA.data +'" added!')
            project_list=check.many_project()
            return render_template('mngt/new_project.html', 
                                    form=form, form2=form2, 
                                    project_list=project_list, 
                                    username=check.username)
        else:
            flash('A project already exists with that name.')
    if form2.validate_on_submit() and form2.submit2.data:
        
        project= check.one_project(name=form2.project_nameB.data)
        reviews=Reviews.query.filter_by(project_id=project.id).all()
        if reviews:
            review=Reviews.query.filter_by(project_id=project.id).first()
            review_name=review.review_name
        else:
            review_name=str(project.project_name)+":_Review_Iteration__0"
            create_new_review=Reviews(review_name=review_name, project_id=project.id)
            db.session.add(create_new_review)
            db.session.commit()
        return redirect(url_for("mngt.new_review",project_name=form2.project_nameB.data, review_name=review_name)) 
    
    elif form2.validate_on_submit() and form2.submit3.data:
        project=check.one_project(name=form2.project_nameB.data)
        db.session.delete(project)
        db.session.commit()
        project_list=check.many_project()
        flash('Project Name "'+form2.project_nameB.data +'" deleted!')
        return render_template('mngt/new_project.html', 
                                form=form, form2=form2, 
                                project_list=project_list, 
                                username=check.username)
    if project_list:
        return render_template('mngt/new_project.html', 
                                form=form, form2=form2, 
                                project_list=project_list, 
                                username=check.username)
    return render_template('mngt/new_project.html', form=form, form2=form2, username=check.username)


@manage_reviews_bp.route('/<project_name>/<review_name>', methods=['GET', 'POST'])
@login_required
def new_review(project_name,review_name):
    check=Check(current_user)
    ### Start Forms
    form1=Edit_Review_Name_Form();  form2=Manage_Review_Form()
    ### Load data from DB
    project=check.one_project(name=project_name)
    current_review=check.one_review(rname=review_name)
    reviews=check.many_review()
    form2.review_names.choices= [(revy.review_name,revy.review_name) for revy in reviews]
    ###Modifiy review name form
    if form1.validate_on_submit() and form1.submit4.data:
        if not current_review:
            current_review=check.one_review()
        review_name=form1.new_review_name.data+"_Iteration__0"
        current_review.review_name=review_name
        db.session.add(current_review)
        db.session.commit()
        return redirect(url_for("mngt.new_review",
                                project_name=project_name, 
                                review_name=review_name))
    
    if form2.validate_on_submit():
        review_name=form2.review_names.data
        ###Open review 
        if form2.submit5.data:
            return redirect(url_for("mngt.review_details",
                                    project_name=project_name, 
                                    review_name=review_name))
        
        elif form2.submit6.data:
            ###Delete review name form
            selected_review= check.one_review(rname=review_name)
            db.session.delete(selected_review)
            db.session.commit()
            review=check.one_review()
            review_name=review.review_name
            return redirect(url_for("mngt.new_review",
                                project_name=project_name, 
                                review_name=review_name))
            
        elif form2.submit7.data:
            #Add New Review Itereration
            cod='_Iteration__'
            selected_review= check.one_review(rname=review_name)
            iter_name=selected_review.review_name
            review_name=iter_name.split(cod)[0]+cod+str(int(iter_name.split(cod)[1])+1)
            create_new_review=Reviews(review_name=review_name, project_id=project.id)
            db.session.add(create_new_review)
            db.session.commit()
            return redirect(url_for("mngt.new_review",
                                    project_name=project_name, 
                                    review_name=review_name))

    return render_template('mngt/new_review.html', 
                            username=check.username, 
                            project_name=project_name, 
                            review_name=review_name,
                            form1=form1 , form2=form2)
    
@manage_reviews_bp.route('/<project_name>/<review_name>/review_details', methods=['GET', 'POST'])
@login_required
def review_details(project_name,review_name):
    check=Check(current_user)
    project = check.one_project(name=project_name)
    review = check.one_review(rname=review_name)

    formA=Problem_Space_Form(); formB=Solution_Space_Form();
    formC=Total_Group_Form();
    formC.tt_groups.choices= [(1,"one"),(2,"two"),(3,"three"),(4,"four")]
    

    if formA.validate_on_submit() and formA.submit8.data:
        ptext=formA.problem_space_text.data
        review.problem_space_text=ptext
        db.session.add(review)
        db.session.commit()

    if formB.validate_on_submit() and formB.submit9.data:
        stext=formB.solution_space_text.data
        review.solution_space_text=stext
        db.session.add(review)
        db.session.commit()
        
    if formC.validate_on_submit() and formC.submit10.data:
        tt_groups=formC.tt_groups.data
        review.tt_groups=tt_groups
        db.session.add(review)
        db.session.commit()

    if review.group_name==None:
        review.group_name='{"group_A":"Empty", "group_B":"Empty", "group_C":"Empty", "group_D":"Empty"}'
        db.session.add(review)
        db.session.commit()

    formD=Add_Group_Form_A(); formE=Add_Group_Form_B()
    formF=Add_Group_Form_C(); formG=Add_Group_Form_D()

    if formD.validate_on_submit() and formD.submit11.data:
        group_name1=formD.group_name1.data
        group_name_dict=eval(review.group_name)
        group_name_dict["group_A"]=group_name1
        review.group_name=str(group_name_dict) 
        db.session.add(review) 
        db.session.commit()

    if review.tt_groups ==2:
        if formE.validate_on_submit() and formE.submit12.data:
            group_name2=formE.group_name2.data
            group_name_dict=eval(review.group_name)
            group_name_dict["group_B"]=group_name2
            review.group_name=str(group_name_dict) 
            db.session.add(review) 
            db.session.commit()

    if review.tt_groups ==3:
        
        if formF.validate_on_submit() and formF.submit13.data:
            group_name3=formF.group_name3.data
            group_name_dict=eval(review.group_name)
            group_name_dict["group_C"]=group_name3
            review.group_name=str(group_name_dict) 
            db.session.add(review) 
            db.session.commit()
        
    if review.tt_groups ==4:
        
        if formG.validate_on_submit() and formG.submit14.data:
            group_name4=formF.group_name4.data
            group_name_dict=eval(review.group_name)
            group_name_dict["group_D"]=group_name4
            review.group_name=str(group_name_dict) 
            db.session.add(review) 
            db.session.commit()
    group_name_dict=eval(review.group_name)
    return render_template('mngt/review_details.html', 
                            username=check.username, project_name=project_name, 
                            review_name=review_name,
                            formA=formA, formB=formB, formC=formC, formD=formD,
                            formE=formE, formF=formF, formG=formG, group_name_dict=group_name_dict,
                            review=review)

@manage_reviews_bp.route('/share_project')
def share_project():
    wmi=Wmi(current_user);  user_id=wmi.get_user_id();  username=wmi.get_username()
    ### to be defined
    return render_template('mngt/share_project.html', username=check.username)