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
    submit = SubmitField("Add Expense")
