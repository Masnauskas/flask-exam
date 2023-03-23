import os
from app import app
from flask import render_template, request, url_for, redirect, flash
from datetime import datetime
import secrets
from PIL import Image
from app import models, forms, db, app
from app.__init__ import bcrypt
from flask_login import current_user, logout_user, login_user, login_required

@app.route('/login')
@app.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('groups'))
        else:
           
            flash('Login error. Please check your email or password')
    
    return render_template('public/login.html', title='Login', form=form)