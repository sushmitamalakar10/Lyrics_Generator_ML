from flask import flash
from flask import Blueprint, render_template, redirect, session, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tbl_users (email, password) VALUES (%s, %s)', (email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tbl_users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[2], password):  # password is at index 2
            session['email'] = email
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
        
        
    return render_template('login.html', form=form)

@main.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    return render_template('dashboard.html')
