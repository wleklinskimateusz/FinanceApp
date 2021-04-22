from flaskr import db, login_manager
from flask import render_template, redirect, url_for, Response, current_app as app
from .forms import CategoryForm, ExpenseForm, LoginForm, StudentForm, PaymentForm, LessonForm
from .models import Category, User, Expense, Student, Lesson, Payment
from flask_login import current_user, login_required, logout_user, login_user
import io













