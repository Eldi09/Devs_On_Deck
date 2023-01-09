from flask_app import app
from flask_app.models import organization, user
from flask import render_template, redirect, request, session, flash, jsonify
import os
from flask_bcrypt import Bcrypt
import re
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException, NotFound
from decimal import Decimal
import uuid as uuid
UPLOAD_FOLDER = 'flask_app/static/css/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
bcrypt = Bcrypt(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/org_register')
def org_register():
    return render_template('org_register.html')

@app.route('/getOrg')
def getOrg():
    emails = organization.Organization.getOrgEmail()
    return jsonify(emails)

@app.route('/create_org', methods = ['POST'])
def createOrg():
    data = {
        'org_name': request.form['org_name'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    organization.Organization.createOrganization(data)
    return redirect('/org_register')

@app.route('/login_org', methods = ['POST'])
def login_org():
    data = {
        'email': request.form['email']
    }
    org_in_db = organization.Organization.get_org_by_email(data)
    if not org_in_db:
        flash("*Invalid Email/Password", "emailOrgLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(org_in_db['password'], request.form['password']):
        flash("*Incorrect password", "pswOrgLogin")
        return redirect(request.referrer)
    session['org_id'] = org_in_db['id']
    return redirect('/org_dashboard')

@app.route('/org_login')
def org_login():
    if 'user_id' in session:
        return redirect('/org_dashboard')
    return render_template('orgLogin.html')

@app.route('/org_dashboard')
def org_dashboard():
    if 'org_id' in session:
        data = {
            'org_id': session['org_id']
        }
        loggedUser = organization.Organization.get_org_by_id(data)
        positions = organization.Organization.get_positions(data)
        all_devs = user.User.get_all_devs()
        skills = user.User.get_skills()
        frameworks = user.User.get_frameworks()
        return render_template("org_dashboard.html", loggedUser = loggedUser, positions = positions, all_devs = all_devs, skills = skills, frameworks = frameworks)
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/log_out')

@app.route('/org_profile')
def org_profile():
    if 'org_id' in session:
        data = {
            'org_id': session['org_id']
        }
        loggedUser = organization.Organization.get_org_by_id(data)
        skills = user.User.get_all_skills()
        positions = organization.Organization.get_positions(data)
        all_pos_applied = user.User.get_all_pos_applied(data)
        all_devs = user.User.get_all_devs()
        frameworks = user.User.get_all_frameworks()
        return render_template('orgProfile.html', loggedUser = loggedUser, skills = skills, positions = positions, all_pos_applied =all_pos_applied, all_devs = all_devs, frameworks = frameworks)
    return redirect('/log_out')

@app.route('/create_position', methods = ['POST'])
def create_positions():
    if 'org_id' not in session:
        return redirect('/log_out')
    print(request)
    data = {
        'org_id': session['org_id'],
        'name': request.form['position_name'],
        'description': request.form['description'],
        'skill_1': request.form['skill_1'],
        'skill_2': request.form['skill_2'],
        'skill_3': request.form['skill_3'],
        'skill_4': request.form['skill_4'],
        'skill_5': request.form['skill_5'],
        'frame_1': request.form['frame_1'],
        'frame_2': request.form['frame_2'],
        'frame_3': request.form['frame_3'],
        'frame_4': request.form['frame_4'],
        'frame_5': request.form['frame_5']
    }
    if len(data['name']) < 3:
        flash("*Position name mus belonger than 3 char", 'namePosError')
        return redirect('/org_profile')
    
    if len(data['description']) < 10:
        flash("*Description mus be 10 char or lonerg", 'desError')
        return redirect('/org_profile')
    
    if data['skill_1'] == '':
        flash("*You can not create a position without skills", 'skillOrgError')       
        return redirect('/org_profile')
    if data['frame_1'] == '':
        flash("*You can not create a position without frameworks", 'frameOrgError')       
        return redirect('/org_profile')
    organization.Organization.create_positions(data)
    return redirect(request.referrer)

@app.route('/upload_org_pic', methods = ['POST'])
def upload_org_pic():
    if 'org_id' in session:
        file = request.files['filename']
        if file and allowed_file(file.filename):
            pic_filename = secure_filename(file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            data = {
                'file_path': pic_name,
                'org_id': session['org_id']
            }
            organization.Organization.add_OrgProfile_pic(data)
            return redirect('/org_profile')
        else:
            flash('*This image is not in the right format', 'profile_pic')
            return redirect(request.referrer)
    return redirect('/log_out')

@app.route('/check_skill')
def check_skill():
    skills = user.User.get_all_skills()
    return jsonify(skills)

@app.route('/check_framework')
def check_framework():
    frameworks = user.User.get_all_frameworks()
    return jsonify(frameworks)

@app.route('/show_pos/<int:id>')
def show_pos(id):
    if 'org_id' not in session:
        return redirect('/log_out')
    data = {
            'org_id': session['org_id'],
            'pos_id': id
        }
    match_devs = []
    the_post = organization.Organization.get_pos_by_id(data)
    if the_post == False:
        return redirect('/org_dashboard')
    loggedUser = organization.Organization.get_org_by_id(data)
    all_devs = user.User.get_all_devs()
    post_skills = [the_post['skill_1'],the_post['skill_2'],the_post['skill_3'],the_post['skill_4'],the_post['skill_5']]
    num_of_skill = 0
    for skill in post_skills:
        if skill != 'n/a' and skill != 'undefined':
            num_of_skill = num_of_skill + 1
    for dev in all_devs:
        dev_skill = []
        count = 0
        data = {
            'dev_id': dev['id']
        }
        info = {}
        result = user.User.get_dev_skills(data)
        for row in result:
            dev_skill.append(row['skill'])
        for skill in dev_skill:
            for post_skill in post_skills:
                if skill == post_skill:
                    count = count + 1
        if count >= 1:
            count1 = str(round((count/num_of_skill)*100, -1))
            count1 = count1.replace('.0', '')
            info = {
                'id': dev['id'],
                'first_name': dev['first_name'],
                'last_name': dev['last_name'],
                'skills': dev_skill,
                'profile_pic': dev['profile_pic'],
                'count': int(count1)
            }
            match_devs.append(info)

    skills = user.User.get_all_skills()
    return render_template('show_position.html', loggedUser = loggedUser, the_post = the_post, skills = skills, match_devs =match_devs, post_skills = post_skills)

@app.route('/show_user/<int:id>')
def show_user(id):
    if 'org_id' not in session:
        return redirect('/log_out')
    data = {
        'dev_id': id,
        'org_id': session['org_id']
    }
    dev_skills = user.User.get_dev_skills(data)
    dev_frameworks = user.User.get_dev_frameworks(data)
    communication = organization.Organization.get_communications(data)
    the_user = user.User.get_user_by_id(data)
    loggedUser = organization.Organization.get_org_by_id(data)
    skills = user.User.get_all_skills()
    if communication:
        data['communication_id'] = communication[0]['id']
        messages = organization.Organization.get_messages(data)
        frameworks = user.User.get_all_frameworks()
        return render_template('show_user.html', loggedUser = loggedUser, the_user = the_user, skills = skills,
        dev_skills = dev_skills, dev_frameworks = dev_frameworks, communication = communication, messages = messages)
    return render_template('show_user.html', loggedUser = loggedUser, the_user = the_user, skills = skills,
        dev_skills = dev_skills, dev_frameworks = dev_frameworks)
    

@app.route('/accept/<int:dev_id>/<int:pos_id>')
def accept(dev_id, pos_id):
    if 'org_id' not in session:
        return redirect('log_out')
    data = {
        'dev_id': dev_id,
        'pos_id': pos_id,
        'org_id': session['org_id'],
        'status': 1
    }
    organization.Organization.update_status(data)
    return redirect('/org_profile')

@app.route('/reject/<int:dev_id>/<int:pos_id>')
def reject(dev_id, pos_id):
    if 'org_id' not in session:
        return redirect('log_out')
    data = {
        'dev_id': dev_id,
        'pos_id': pos_id,
        'org_id': session['org_id'],
        'status': 0
    }
    organization.Organization.update_status(data)
    return redirect('/org_profile')

@app.route('/create_communications/<int:id>')
def create_communications(id):
    if 'org_id' not in session:
        return redirect('log_out')
    data = {
        'dev_id': id,
        'org_id': session['org_id']
    }
    comunication = organization.Organization.get_communications(data)
    if comunication:
        return redirect(request.referrer)
    organization.Organization.create_communications(data)
    return redirect(request.referrer)

@app.route('/send_message/<int:id>', methods = ['POST'])
def send_message(id):
    if 'org_id' in session:
        data = {
            'dev_id': id,
            'org_id': session['org_id'],
            'message': request.form['message']
        }
        org = organization.Organization.get_org_by_id(data)
        dev = organization.Organization.get_user(data)
        communication = organization.Organization.get_communications(data)
        data['sender'] = org['org_name']
        data['receiver'] = dev['first_name'] + " " + dev['last_name']
        data['communication_id'] = communication[0]['id']
        organization.Organization.send_message(data)
        return redirect(request.referrer)
    
    if 'user_id' in session:
        data = {
            'dev_id': session['user_id'],
            'org_id': id,
            'message': request.form['message']
        }
        org = organization.Organization.get_org_by_id(data)
        loggedUser = user.User.get_user_by_id(data)
        communication = organization.Organization.get_communications(data)
        data['sender'] = loggedUser['first_name'] + " " + loggedUser['last_name']
        data['receiver'] = org['org_name']
        data['communication_id'] = communication[0]['id']
        organization.Organization.send_message(data)
        return redirect(request.referrer)
    return redirect('log_out')