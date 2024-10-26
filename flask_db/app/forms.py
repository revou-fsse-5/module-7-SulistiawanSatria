from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=6)])
    
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another one.')