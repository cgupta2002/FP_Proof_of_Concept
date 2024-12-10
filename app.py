from flask import Flask, render_template, url_for, request, redirect, flash, session
from werkzeug.utils import secure_filename
from users import User
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = '2bshd9ei3nd40fk'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    return render_template('index.html', user=user, user_id=user_id)

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
