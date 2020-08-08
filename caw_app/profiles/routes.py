import os
from flask import Flask, flash, request, redirect, url_for,render_template, current_app
from werkzeug.utils import secure_filename
from caw_app.profiles import profiles_bp
from caw_app.profiles.forms import SimpleEmailForm, NameForm, UploadImageForm
from caw_app.models import Wmi
from flask_login import current_user
from caw_app import db



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profiles_bp.route('/<username>', methods=['GET', 'POST'])
def user_profile(username):
    wmi=Wmi(current_user); user=wmi.get_user()
    eform=SimpleEmailForm();    nform=NameForm();    iform=UploadImageForm()

    if eform.validate_on_submit():
        user.email=eform.email.data
        db.session.add(user)
        db.session.commit()

    if nform.validate_on_submit():
        user.name=nform.fullname.data
        db.session.add(user)
        db.session.commit()

    if iform.validate_on_submit():
        photo = iform.photo.data
        
        #if photo and allowed_file(photo.filename):
            #filename = secure_filename(photo.filename)
            #basedir = os.path.abspath(os.path.dirname(__file__))
            #new_path = os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename)
            #photo.save(new_path)
            #photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'],user.username, filename))
            #user_folder=os.path.normpath("/user_data/"+user.username+"/")
            
            #new_path=new_path.replace('\\','/')
            #flash(new_path)
            
            #if not os.path.exists(new_path):
            #    os.mkdir(new_path)
            #full_path=new_path+os.path.normpath("/"+filename)
            #user.profile_image_path=full_path    
            #db.session.add(user)
            #db.session.commit()
            #photo.save(new_path)
            #flash(photo.save(new_path))

    return render_template('profiles/my_profile.html', title='User Profile', 
                            eform=eform, nform=nform, iform=iform,
                            username=username, user=user)
    