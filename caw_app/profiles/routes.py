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
        f = request.files['photo']
        filename = secure_filename(f.filename)
        dest=current_app.config['UPLOADS_DEFAULT_DEST']
        url=current_app.config['UPLOADS_DEFAULT_URL']
        flash(dest)
        flash(url)
        if not os.path.exists(dest):
            os.mkdir(dest)

        filepath = dest+filename; urlpath = url+filename
        f.save(filepath)
        flash("filepath"); flash(filepath)
        flash("url");      flash(urlpath)
        user.profile_image_path=urlpath
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, your item has been added")

    return render_template('profiles/my_profile.html', title='User Profile', 
                            eform=eform, nform=nform, iform=iform,
                            username=username, user=user)
    