from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CategoryForm(FlaskForm):
    label = StringField("Label", validators=[DataRequired()])
    submit = SubmitField("Add Category")


class ExpenseForm(FlaskForm):
    label = StringField("Label", validators=[DataRequired()])
    cost = FloatField("Cost", validators=[DataRequired()])
    category = SelectField(u'Category', coerce=int)
    date = DateField("Date", default=datetime.utcnow())
    refund = BooleanField("Refund")
    split = BooleanField("Split")
    split_with = SelectField(u'Users', coerce=int)
    submit = SubmitField("Add Expense")


class StudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    hourly_rate = FloatField("Hourly Rate")
    messenger_link = StringField("Messenger link")
    submit = SubmitField("Add Student")


class PaymentForm(FlaskForm):
    student = SelectField(u'Student', coerce=int)
    value = FloatField()
    date = DateField(default=datetime.utcnow())
    submit = SubmitField("Add Payment")


class LessonForm(FlaskForm):
    student = SelectField(u'Student', coerce=int)
    topic = StringField("Topic")
    date = DateField(default=datetime.utcnow())
    submit = SubmitField("Add Lesson")

