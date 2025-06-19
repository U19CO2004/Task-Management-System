from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
# app/auth/forms.py

# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Email

# class ForgotPasswordForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Reset Password')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=3, message="Password must be at least 3 characters long.")
    ])
    
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=25, message="Username must be between 3 and 25 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=3, message="Password must be at least 3 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    role = SelectField('Role', choices=[
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ], validators=[DataRequired(message="Please select a role.")])
    
    submit = SubmitField('Register') 

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

