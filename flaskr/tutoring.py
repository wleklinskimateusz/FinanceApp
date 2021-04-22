from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)
from flask_login import current_user

from .forms import CategoryForm, ExpenseForm, PaymentForm, LessonForm, StudentForm
from .models import Category, Expense, User, Payment, Student, Lesson
from . import db

bp = Blueprint('tutoring', __name__)


@bp.route('/tutoring')
def tutoring():

    return render_template('tutoring.html', tutoring=True, summary_active=True)


@bp.route('/tutoring/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()
    if form.validate_on_submit():
        s = Student()
        s.name = form.name.data
        s.hourly_rate = form.hourly_rate.data
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('tutoring.students'))

    return render_template('students.html', tutoring=True, form=form, students=Student.query.all(), students_active=True)


@bp.route('/tutoring/students/<int:student_id>')
def student(student_id):
    return render_template(
        'student.html',
        student=Student.query.filter_by(id=student_id).first(),
        students_active=True
    )


@bp.route('/tutoring/lessons', methods=['GET', 'POST'])
def lessons():
    form = LessonForm()
    form.student.choices = [(s.id, s.name) for s in Student.query.all()]
    if form.validate_on_submit():
        lesson = Lesson()
        lesson.topic = form.topic.data
        lesson.student = form.student.data
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('tutoring.lessons'))
    return render_template('lessons.html', form=form, students=Student.query.all(), Lesson=Lesson, lessons_active=True)


@bp.route('/tutoring/payments', methods=['GET', 'POST'])
def payments():
    form = PaymentForm()
    form.student.choices = [(s.id, s.name) for s in Student.query.all()]
    if form.validate_on_submit():
        payment = Payment()
        payment.student = form.student.data
        payment.date = form.date.data
        payment.value = form.value.data
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('tutoring.payments'))
    return render_template('payments.html', students=Student.query.all(), form=form, Payment=Payment, payments_active=True)


@bp.route('/tutoring/payments/<int:payment_id>')
def payment(payment_id):
    return render_template(
        'payment.html',
        payment=Payment.query.filter_by(id=payment_id).first(),
        Student=Student,
        payments_active=True
    )

