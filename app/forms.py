from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from app import models, current_user, app



class RegistrationForm(FlaskForm):
    name = StringField('Name:', [DataRequired()])
    email = StringField('Email:', [Email(message=('Email entered wrong.')), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField("Repeat your password",
                                             [EqualTo('password', "Passwords must be the same.")])
    submit = SubmitField('Submit')
    

    def check_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please enter another email.')
        
        
class LoginForm(FlaskForm):
    email = StringField('Email:', [Email(message=('Email entered wrong.')), DataRequired()])
    password = PasswordField('Password:', [DataRequired()])
    remember_me = BooleanField("Remember")
    submit = SubmitField('Login')

class AddGroupBillForm(FlaskForm):
    name = StringField('Expense group name:', [DataRequired()])
    submit = SubmitField('Add')
    
class AddBillsForm(FlaskForm):
    description = StringField('Description:', [DataRequired()])
    price = FloatField('Amount:', [DataRequired()])
    submit = SubmitField('Add')
    
class ProfileForm(FlaskForm):
    name = StringField('Name:', [DataRequired()])
    email = StringField('Email:', [DataRequired()])
    submit = SubmitField('Submit')
    
    def check_email(self, email):
        if email.data != current_user.email:
            user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email in use. Please enter another email address')
        
class RequestResetForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('User not found. Please register.')
        
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat your password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
    