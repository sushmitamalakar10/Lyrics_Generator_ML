from flask import flash
from flask import Blueprint, render_template, redirect, session, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm, LyricsForm
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
        
        flash('Registered successfully! Please log in.', 'success')

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
            session['user_id'] = user[0]
            session['email'] = user[1]
            
            flash('Logged in successfully!', 'success')
            
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
        
        
    return render_template('login.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('main.login'))
    
    form = LyricsForm()
    
    if form.validate_on_submit():
        prompt = form.prompt.data
        genre = form.genre.data
        length = form.length.data
        uid = session['user_id']
        
        generated_lyrics = f"Generated lyrics for prompt: {prompt}, genre: {genre}, length: {length}"
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO tbl_lyrics (uid, prompt, genre, length, lyrics) VALUES (%s, %s, %s, %s, %s)",
            (uid, prompt, genre, length, generated_lyrics)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Lyrics generated and saved!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', form=form)

@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.login'))

