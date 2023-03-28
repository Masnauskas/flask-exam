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

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    user_id = current_user.id
    form = forms.AddGroupBillForm()
    data = models.Group.query.filter_by(user_id=user_id)
    if form.validate_on_submit():
            dateNow = datetime.now()
            dateNowFormatted = dateNow.strftime("%d/%m/%Y %H:%M:%S")
            group_entry = models.Group(
                                name=form.name.data,
                                date = dateNowFormatted,
                                user_id = user_id
                                )
            db.session.add(group_entry)
            db.session.commit()
            flash('Expenditure successfully added.')
            return redirect(url_for('groups', user_id=user_id))
    return render_template('public/groups.html', title='Groups', form=form, data=data, user = user_id)


@app.route('/<int:group_id>/', methods=('GET', 'POST'))
@login_required
def bills(group_id):
    group = models.Group.query.get_or_404(group_id)
    form = forms.AddBillsForm()
    if form.validate_on_submit():
        bill = models.Bills(description=form.description.data,
                            price=form.price.data,
                           group_id=group_id
                            )
        db.session.add(bill)
        db.session.commit()
   
        return redirect(url_for('bills', group_id=group.id))
    return render_template('public/bills.html', title='Bills', group = group, form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500

@app.route("/profile", methods=('GET', 'POST'))
@login_required
def profile():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('public/profile.html', title='Profile', form=form)