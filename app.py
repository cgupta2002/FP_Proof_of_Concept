from flask import Flask, render_template, url_for, request, redirect, flash, session
from werkzeug.utils import secure_filename
from users import User
from projects import Project
from machines import Machine
from unifiedData import DataStream
import os
from datetime import datetime, date
import sqlite3
import ast

app = Flask(__name__)
app.secret_key = '09safkj3784hjfrk9'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    return render_template('index.html', user=user, user_id=user_id)

@app.route('/projects')
def projects():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    projects = Project.getAllProjects()
    return render_template('projects.html', user=user, user_id=user_id, projects=projects)


@app.route('/alerts')
def alerts():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    machines = Machine.getAllMachines()    
    return render_template('alerts.html', user=user, user_id=user_id, machines=machines)

@app.route('/alerts/<machine_id>')
def alert(machine_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    conn = sqlite3.connect('db_path.db')
    machine = Machine.getMachine(machine_id)
    cursor = conn.cursor()
    cursor.execute('SELECT history FROM machines where machine_id=?',(machine_id,))
    result = cursor.fetchone()
    if result and result[0]:  
        history_str = result[0]
        try:
            history = ast.literal_eval(history_str)
            print(f"Extracted history: {history}")
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing history: {e}")
            history = []
    else:
        print("No history found for the specified machine.")
        history = []
    conn.close()
    return render_template('alert.html', user=user, user_id=user_id, machine=machine, history=history)

@app.route('/alerts/add', methods=['GET', 'POST'])
def add_machine():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        return render_template('add_machine.html', user=user, user_id=user_id, status='ADD-MACHINE')
    elif request.method == 'POST':
        machine_id = request.form['machine_id']
        name = request.form['name']
        type = request.form['type']
        status = request.form.get('status')
        notes = request.form['notes']
        last_update = datetime.now()
        Machine.addMachine(machine_id,name, type, status, notes, last_update)
        return redirect(url_for('alerts', user_id=user_id))
    

@app.route('/alerts/<machine_id>/edit', methods=['GET','POST'])
def edit_machine(machine_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    machine = Machine.getMachine(machine_id)
    if request.method == 'GET':
        return render_template('add_machine.html', user=user, user_id=user_id, machine_id = machine_id, machine=machine, status='EDIT-MACHINE')
    elif request.method == 'POST':
        machine_id = request.form['machine_id']
        name = request.form['name']
        type = request.form['type']
        status = request.form.get('status')
        print(status)
        notes = request.form['notes']
        last_update = datetime.now().replace(microsecond=0)
        Machine.updateMachine(machine_id,name, type, status, notes, last_update)
        return redirect(url_for('alerts', user_id=user_id))

@app.route('/delete')
def delete_machine(machine_id=None):
    user_id = session.get('user_id')
    Machine.delMachine(machine_id)
    return redirect(url_for('alerts', user_id=user_id))

@app.route('/analytics')
def analytics():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    datastreams = DataStream.getAllDataStreams()
    return render_template('analytics.html', user=user, user_id=user_id, datastreams=datastreams)

@app.route('/analytics/add', methods=['GET', 'POST'])
def add_ds(datastream_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        return render_template('add_datastream.html',status='ADD-DS', user_id=user_id, user=user)
    elif request.method == 'POST':
        datastream_id = request.form['datastream_id']
        name = request.form['name']
        department = request.form['department']
        process_time = request.form['process_time']
        poc_name = request.form['poc_name']
        poc_email = request.form['poc_email']
        poc_phone = request.form['poc_phone']
        status = request.form.get('status')
        last_update = datetime.now().replace(microsecond=0)
        DataStream.addDataStream(datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone)
        return redirect('analytics.html', user_id=user_id, user=user)

@app.route('/analytics/<datastream_id>/edit', methods=['GET', 'POST'])
def edit_ds(datastream_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        ds = DataStream.getDataStream(datastream_id)
        return render_template('add_datastream.html', status='EDIT-DS',user_id=user_id, user=user, datastream = ds)
    elif request.method == 'POST':
        datastream_id = request.form['datastream_id']
        name = request.form['name']
        department = request.form['department']
        process_time = request.form['process_time']
        poc_name = request.form['poc_name']
        poc_email = request.form['poc_email']
        poc_phone = request.form['poc_phone']
        status = request.form.get('status')
        last_update = datetime.now().replace(microsecond=0)
        DataStream.updateDataStream(datastream_id, name, department, process_time, status, last_update, poc_name, poc_email, poc_phone)
        return redirect('analytics.html', user_id=user_id, user=user)

    
@app.route('/analytics/<datastream_id>/edit', methods=['GET', 'POST'])
def delete_ds(datastream_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    DataStream.delDataStream(datastream_id)
    return redirect(url_for('analytics'))


@app.route('/analytics/<datastream_id>')
def datastream(datastream_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    datastream = DataStream.getDataStream(datastream_id)
    return render_template('datastream.html', user=user, user_id=user_id, datastream=datastream, datastream_id=datastream_id)


@app.route('/projects/<int:project_id>')
def project(project_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    project = Project.getAllProjects()
    for item in project:
        if item['project_id'] == project_id:
            proj = item
    budget_difference = proj['budget'] - proj['curr_exp']
    return render_template('project.html', user=user, user_id=user_id, project=proj, budget_difference=budget_difference)

@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        return render_template('add_project.html', user=user, user_id=user_id, status='ADD')
    elif request.method == 'POST':
        projects = Project.getAllProjects()
        project_id = (projects[-1]['project_id']) +1
        name = request.form['name']
        location = request.form['location']
        est_length = request.form['est_length']
        start_date = request.form['start_date']
        proj_end = request.form['proj_end']
        budget = request.form['budget']
        curr_exp = request.form['curr_exp']
        poc_name = request.form['poc_name']
        poc_email = request.form['poc_email']
        poc_phone = request.form['poc_phone']
        status = request.form.get('status')
        Project.addProject(project_id,name, poc_name,poc_email,poc_phone,location,est_length,budget,curr_exp,start_date,proj_end,status)
        return redirect(url_for('project', project_id = project_id))


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    return render_template('profile.html', user=user, user_id=user_id)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        users = User.getAllUsers()
        last_id = int(users[-1]['user_id'])
        user_id = last_id + 1
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        profile_image = request.files['profile_image']
        print(profile_image)
        branch = request.form['branch']
        name = (str(fname) +' '+ str(lname)).title()
        session['user_id'] = user_id
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            filepath = "static/images/" + filename
            filepath = filepath.replace("\\", "/")
            profile_image.save(filepath)
            if not username or not password or not fname or not lname or not email or not branch:
                flash('All required fields must be filled out.', 'error')
                return redirect(url_for('registration'))
            else:
                User.addUser(user_id, username, name, email, password, filename, branch)
                user = User.getUserByID(user_id)
                return redirect(url_for('index', user_id=user_id, user=user))
        elif not profile_image:
            User.addUserNoPic(user_id, username, name, email, password, branch)
            user = User.getUserByID(user_id)
            return redirect(url_for('index', user_id=user_id, user=user))
        else:
            flash('Invalid file format. Please upload an image.')
            return redirect(url_for('registration'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Username and Password are required.', 'error')
            return redirect(url_for('login'))
        user = User.getUser(username)
        if user:
            user_id = user['user_id']
            if user['password'] == password:
                session['user_id'] = user['user_id']
                user_id = user['user_id']
                return redirect(url_for('index', user_id=user_id, user=user, profile_image = user['profile_image']))
            else:
                users = User.getAllUsers()
                return render_template('login.html', error="Invalid password.", users=users)
        else:
            users= User.getAllUsers()
            return render_template('login.html', error="User does not exist. Did you mean to register?", users=users)            
    if request.method == 'GET':
        users = User.getAllUsers()
        return render_template('login.html', users=users)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    User.createUserTable()
    User.InsertStartingData()
    app.run(debug=True)
