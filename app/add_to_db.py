from app import db
from app.models import Group, Bills

group1 = Group(name='Our trip to SF')
group2 = Group(name='Our trip to NY')
group3 = Group(name='Our trip to LA')
group4 = Group(name='Our trip to Miami')
group5 = Group(name='Our trip to Chicago')
group6 = Group(name='Our trip to Las Vegas')
group7 = Group(name='Our trip to Atlanta')

db.session.add_all(group1, group2, group3, group4, group5, group6, group7)
db.session.commit()