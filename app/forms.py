from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from app import models, current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name:', [DataRequired()])
    email = StringField('Email:', [Email(message=('Email entered wrong.')), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField("Repeat your password",
                                             [EqualTo('password', "Password must be the same.")])
    image = FileField('Upload your picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')
    

    def check_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please enter another email.')
        
        
class LoginForm(FlaskForm):
    email = StringField('Email:', [Email(message=('Email entered wrong.')), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField("Remember")
    submit = SubmitField('Login')
    
class AddBillsForm(FlaskForm):
    description = StringField('Description:', [DataRequired()])
    price = FloatField('Amount:', [DataRequired()])
    submit = SubmitField('Add')