from database import db
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text, nullable=False)  
    directory = db.Column(db.String, nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    userid = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    tasks = db.relationship('UserTask', back_populates='user')


class UserTask(db.Model):
    __tablename__ = 'user_tasks'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), primary_key=True)
    rights = db.Column(db.Integer, nullable=False) 

    user = db.relationship('User', back_populates='tasks')
    task = db.relationship('Task')

    def has_permission(self, permission):
        return (self.rights & permission) == permission

    def add_permission(self, permission):
        self.rights |= permission

    def remove_permission(self, permission):
        self.rights &= ~permission


def create_database(app):
    with app.app_context():
        db.create_all()
