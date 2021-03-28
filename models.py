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
    label = db.Column(db.String(50))
    cost = db.Column(db.Float)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    refund = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.label}, {self.cost}zł"


### Korki

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    hourly_rate = db.Column(db.Float)
    total = db.Column(db.Float, nullable=True)
    paid = db.Column(db.Float, nullable=True)

    def money_total(self):
        self.total = self.hourly_rate * len(Lesson.query.filter_by(student=self.id).all())
        db.session.commit()
        return self.total

    def money_paid(self):
        self.paid = 0
        for p in Payment.query.filter_by(student=self.id):
            self.paid += p.value
        db.session.commit()
        return self.paid

    def to_pay(self):
        return self.money_total() - self.money_paid()

    def __repr__(self):
        return self.name


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    student = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f"{self.value}zł, {self.date.date()}"


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey('student.id'))
    topic = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.topic}, {self.date.date()}"

