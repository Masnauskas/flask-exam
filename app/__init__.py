import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from flask_bcrypt import Bcrypt

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.app_context().push()
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from app import routes
from app.models import User, Group, Bills

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'registration'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

