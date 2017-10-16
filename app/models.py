from datetime import datetime

from flask import redirect
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from app import inventory_labels, db, admin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('Role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Project(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    wikipage = db.Column(db.String(100))
    logourl = db.Column(db.String(256))

    def __str__(self):
        return self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100))
    product = db.Column(db.String(100))
    serial = db.Column(db.String(100))
    project_name = db.Column(db.String(100), db.ForeignKey('project.name'))
    project = db.relationship('Project', backref='project')
    notes = db.Column(db.Text)
    location = db.Column(db.String(1024))
    user = db.Column(db.String(1024))
    responsible = db.Column(db.String(1024))
    changes = db.relationship('Change', backref='item')

    def __str__(self):
        return "[{}] {} {}".format(self.id, self.manufacturer, self.product)

inventory_labels.Item = Item
inventory_labels.Project = Project




class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30))
    field = db.Column(db.String(256))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    new_value = db.Column(db.Text)
    datetime = db.Column(db.DateTime)

    def __str__(self):
        return "{}: {} changed {} to '{}' on {}".format(self.datetime, self.user, self.field, self.new_value, str(self.item))
