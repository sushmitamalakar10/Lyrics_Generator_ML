# from flask import Flask, render_template, redirect, url_for
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, ValidationError
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_mysqldb import MySQL


# app = Flask(__name__)

# # MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''  # If root has no password, else set it here
# app.config['MYSQL_DB'] = 'lyrics_generator'


# app.secret_key = 'your_secret_key'

# # Initialize MySQL
# mysql = MySQL(app)
# # Registration form

# class RegisterForm(FlaskForm):
#      email = StringField('Email', validators=[DataRequired(), Email()])
#      password = PasswordField('Password', validators=[DataRequired()])
#      submit = SubmitField('Register')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data   
        
#         hashed_password = generate_password_hash(password)

#         cursor = mysql.connection.cursor()
#         cursor.execute('INSERT INTO tbl_users (email, password) VALUES (%s, %s)', (email, hashed_password))
#         mysql.connection.commit()
#         cursor.close()
        
#         return redirect(url_for('login'))
     
        
        
        
        
#     return render_template('register.html', form=form)

# @app.route('/login')    
# def login():
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# if __name__ == "__main__":
#     app.run(debug=True)

