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
    pass