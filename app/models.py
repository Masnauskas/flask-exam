from app import app, db
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import jwt
import os
from time import time
from api_jwt import APIJwt 



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    groups = db.relationship('Group', backref='groups')
    
    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
        
        
    #     return s.dumps({'user_id': self.id}).decode('utf-8')
    
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)
    
    def get_reset_token(self, expires=1000):
        return jwt.encode({'user_id': self.id, 'exp': time() + expires},
                           key=app.config['SECRET_KEY'])
        
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, key=app.config['SECRET_KEY'])['user_id']
            print(user_id)
        except Exception as e:
            print(e)
            return
        return User.query.get(user_id)
    
class Group(db.Model, UserMixin):
    __tablename__ = 'group_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bills = db.relationship('Bills', backref='group_list')
    # ids = db.relationship('User', secondary='ids', backref='group_list')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(80), nullable=False)
   
    
    
class Bills(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group_list.id'))
    

    
# id_table = db.Table('user_groups',
#                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                     db.Column('group_id', db.Integer, db.ForeignKey('group_list.id'))
#                     )    

   
    
  