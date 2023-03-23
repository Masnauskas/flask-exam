import os
from app import app
from flask import render_template, request, url_for, redirect, flash
from datetime import datetime
import secrets
from PIL import Image
from app import models, forms, db, app
from app.__init__ import bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, logout_user, login_user, login_required

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
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

@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    data = models.User.query.all()
    form = forms.RegistrationForm()
    try:
        if form.validate_on_submit():
            dateNow = datetime.now()
            dateNowFormatted = dateNow.strftime("%d/%m/%Y %H:%M:%S")
            hidden_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = models.User(name=form.name.data,
                                email=form.email.data,
                                date = dateNowFormatted,
                                password=hidden_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. You can now login.')
            return redirect(url_for('login'))
            
    except IntegrityError:
        db.session.rollback()
        flash('Email in use. Please enter another email address')
    return render_template('public/register.html', title='Register', form=form)

@app.route('/groups')
@login_required
def groups():
    return render_template('public/groups.html')