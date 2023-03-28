from app import app, db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    groups = db.relationship('Group', backref='groups')
    
    
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

   
    
  