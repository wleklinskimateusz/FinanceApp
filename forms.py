from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired


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
    submit = SubmitField("Add Expense")
