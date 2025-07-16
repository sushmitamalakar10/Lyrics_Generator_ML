from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp
from app import mysql

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE email = %s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError("Email already registered.")
        
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    

class LyricsForm(FlaskForm):
    prompt = TextAreaField('Prompt', validators=[DataRequired(), Length(min=1, message="Prompt cannot be empty")])
    length = StringField('Length', validators=[DataRequired(), Regexp(r'^\d+$', message="Length must be a number")])
    genre = SelectField(
    'Genre',
    choices=[
        ('Alternative', 'Alternative'),
        ('Alternative_Rock', 'Alternative Rock'),
        ('Country', 'Country'),
        ('Dance', 'Dance'),
        ('Dance_Pop', 'Dance Pop'),
        ('Dancehall', 'Dancehall'),
        ('Disco', 'Disco'),
        ('Electronic', 'Electronic'),
        ('Electropop', 'Electropop'),
        ('Folk_Pop', 'Folk Pop'),
        ('Funk_Pop', 'Funk Pop'),
        ('Hip_Hop', 'Hip Hop'),
        ('Pop', 'Pop'),
        ('Pop_Rock', 'Pop Rock'),
        ('R&B', 'R&B'),
        ('Rap', 'Rap'),
        ('Soul', 'Soul'),
        ('Synthpop', 'Synthpop'),
        ('Trap', 'Trap')
    ],
    validators=[DataRequired()]
)
    submit = SubmitField('Generate Lyrics')
