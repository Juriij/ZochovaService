from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    place = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer)  #   0 - low, 1 - medium, 2 - high
    status = db.Column(db.String(20), nullable=False, default="Waiting For Approval") 

    def __repr__(self):
        return f'Článok: {self.title}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')  # teacher/janitor
    password = db.Column(db.String(128), nullable=False)
