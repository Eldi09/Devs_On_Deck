from flask_app import app
from flask_app.models import user, organization
from flask import render_template, redirect, request, session, flash, jsonify
import os
from flask_bcrypt import Bcrypt
import re
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import uuid as uuid


UPLOAD_FOLDER = 'flask_app/static/css/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
bcrypt = Bcrypt(app)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dev_register')
def dev_register():
    return render_template('dev_register.html')


@app.route('/dev_login')
def dev_login():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('devLogin.html')


@app.route('/create_dev', methods = ['POST'])
def create_dev():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user.User.create_dev(data)
    return redirect('/dev_register')

@app.route('/getUser')
def getUser():
    emails = user.User.getUserEmail()
    return jsonify(emails)

@app.route('/login_dev', methods = ['POST'])
def login_dev():
    data = {
        'email': request.form['login_email']
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("*Invalid Email/Password", "emailLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        flash("*Incorrect password", "pswLogin")
        return redirect(request.referrer)
    session['user_id'] = user_in_db['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            'dev_id': session['user_id']
        }
        loggedUser = user.User.get_user_by_id(data)
        dev_skills = user.User.get_dev_skills(data)
        skills = user.User.get_all_skills()
        positions = organization.Organization.get_all_positions()
        applied_pos = user.User.get_pos_applied(data)
        all_users = user.User.get_all_users()
        frameworks = user.User.get_all_frameworks()
        organizations = organization.Organization.get_all_org()
        all_communications = organization.Organization.get_user_communications(data)
        return render_template("dashboard.html", loggedUser = loggedUser, positions = positions, dev_skills = dev_skills,
            skills = skills, applied_pos = applied_pos, all_users = all_users, organizations = organizations, frameworks = frameworks, all_communications = all_communications)
    if 'org_id' in session:
        return redirect('/org_dashboard')
    return redirect('/log_out')

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('dev_login')

@app.route('/dev_profile')
def dev_profile():
    if 'user_id' in session:
        data = {
                'dev_id': session['user_id']
            }
        loggedUser = user.User.get_user_by_id(data)
        user_pic = loggedUser['profile_pic']
        skills = user.User.get_all_skills()
        frameworks = user.User.get_all_frameworks()
        dev_skills = user.User.get_dev_skills(data)
        dev_frameworks = user.User.get_dev_frameworks(data)
        frame_progress = len(dev_frameworks)*20
        progress_of = len(dev_skills)*20
        organizations = organization.Organization.get_all_org()
        applied_pos = user.User.get_pos_applied(data)
        positions_content = []
        all_communications = organization.Organization.get_user_communications(data)
        for pos in applied_pos:
            data['pos_id'] = pos['position_id']
            p_c = organization.Organization.get_pos_by_id(data)
            p_c['status'] = pos['status']
            positions_content.append(p_c)
        return render_template('devProfile.html', loggedUser = loggedUser, skills = skills,
            dev_skills = dev_skills, progress_of = progress_of, applied_pos = applied_pos,
            positions_content = positions_content, organizations = organizations, frameworks = frameworks, dev_frameworks = dev_frameworks,
            frame_progress = frame_progress, all_communications = all_communications)
    return redirect('/log_out')
    
@app.route('/upload_pic', methods = ['POST'])
def upload_pic():
    if 'user_id' in session:
        file = request.files['filename']
        if file and allowed_file(file.filename):
            pic_filename = secure_filename(file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            data = {
                'file_path': pic_name,
                'dev_id': session['user_id']
            }
            user.User.add_profile_pic(data)
            return redirect('/dev_profile')
        else:
            flash('*This image is not in the right format', 'profile_pic')
            return redirect(request.referrer)
    return redirect('/log_out')


@app.route('/add_skill/<int:id>')
def add_skill(id):
    if 'user_id' not in session:
        return redirect('/log_out')
    data = {
        'dev_id': session['user_id'],
        'skill_id': id
    }
    dev_skills = user.User.get_dev_skills(data)
    for row in dev_skills:
        if data['skill_id'] == row['id']:
            flash('*You have this skill already', 'skillExist')
            return redirect('/dev_profile')
    if len(dev_skills) >= 5:
        flash('*You can not add more than 5 skills', category='skillError')
        return redirect('/dev_profile')
    user.User.add_skill(data)
    return redirect('/dev_profile')

@app.route('/add_frame/<int:id>')
def add_frame(id):
    if 'user_id' not in session:
        return redirect('/log_out')
    data = {
        'dev_id': session['user_id'],
        'frame_id': id
    }
    dev_frameworks = user.User.get_dev_frameworks(data)
    for row in dev_frameworks:
        if data['frame_id'] == row['id']:
            flash('*You have this framework already', 'frameExist')
            return redirect('/dev_profile')
    if len(dev_frameworks) >= 5:
        flash('*You can not add more than 5 frameworks', category='frameError')
        return redirect('/dev_profile')
    user.User.add_frame(data)
    return redirect('/dev_profile')

@app.route('/update_user', methods = ['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/log_out')
    
    data = {
        'dev_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    loggedUser = user.User.get_user_by_id(data)
    if not bcrypt.check_password_hash(loggedUser['password'], request.form['password']):
        flash("*Invalid Password", "changePsw")
        return redirect('/dev_profile')
    if data['first_name'] == '':
        data['first_name']=loggedUser['first_name']
    elif data['last_name'] == '':
        data['last_name'] = loggedUser['last_name']
    elif data['email']=='':
        data['email']= loggedUser['email']
    
    data['password'] = loggedUser['password']
    user.User.update_user(data)
    return redirect('/dev_profile')

@app.route('/apply/<int:id>')
def apply(id):
    if 'user_id' not in session:
        return redirect('/log_out')
    data = {
        'dev_id': session['user_id'],
        'pos_id': id
    }
    position = organization.Organization.get_pos_by_id(data)
    data['org_id'] = position['organization_id']
    applied_pos = user.User.get_pos_applied(data)
    for pos in applied_pos:
        if data['pos_id'] == pos['position_id']:
            return redirect('/dashboard')
    user.User.apply(data)
    return redirect('/dashboard')

@app.route('/show_messages/<int:id>')
def show_messages(id):
    if 'user_id' in session:
        data = {
            'dev_id': session['user_id'],
            'org_id': id
        }
        org = organization.Organization.get_org_by_id(data)
        loggedUser = user.User.get_user_by_id(data)
        communication = organization.Organization.get_communications(data)
        data['communication_id'] = communication[0]['id']
        messages = organization.Organization.get_messages(data)
    return render_template('show_messages.html', loggedUser = loggedUser, messages = messages, communication = communication, org = org)