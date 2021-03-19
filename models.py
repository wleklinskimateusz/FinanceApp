from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    joined = db.Column(db.DateTime(), index=True, default=datetime.utcnow())
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(32), index=True, unique=True)

    def __repr__(self):
        return self.label


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, index=True, unique=True)
    cost = db.Column(db.Float, index=True, unique=True)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.label}, {self.cost}zł"

