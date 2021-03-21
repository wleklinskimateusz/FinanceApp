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
    month_sum = db.Column(db.Float, default=0)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.label

    def summary(self):
        output = 0
        for ex in Expense.query.filter_by(category=self.id, user=self.owner):
            output += ex.cost

        self.month_sum = output
        db.session.commit()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    cost = db.Column(db.Float)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    refund = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.label}, {self.cost}zł"

