from flaskr import db, login_manager
from flask import render_template, redirect, url_for, Response, current_app as app
from .forms import CategoryForm, ExpenseForm, LoginForm, StudentForm, PaymentForm, LessonForm
from .models import Category, User, Expense, Student, Lesson, Payment
from flask_login import current_user, login_required, logout_user, login_user
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure








@app.route('/plot.png')
def plot_png():
    ID = None
    if current_user.is_authenticated:
        ID = current_user.id
    for cat in Category.query.filter_by(owner=ID):
        cat.summary()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = [cat.label for cat in Category.query.filter_by(owner=ID)]
    ys = [cat.month_sum for cat in Category.query.filter_by(owner=ID)]
    axis.bar(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/tutoring')
def tutoring():

    return render_template('tutoring.html', tutoring=True, summary_active=True)


@app.route('/tutoring/students', methods=['GET', 'POST'])
def students():
    form = StudentForm()
    if form.validate_on_submit():
        s = Student()
        s.name = form.name.data
        s.hourly_rate = form.hourly_rate.data
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('students'))

    return render_template('students.html', tutoring=True, form=form, students=Student.query.all(), students_active=True)


@app.route('/tutoring/students/<int:student_id>')
def student(student_id):
    return render_template(
        'student.html',
        student=Student.query.filter_by(id=student_id).first(),
        students_active=True
    )


@app.route('/tutoring/lessons', methods=['GET', 'POST'])
def lessons():
    form = LessonForm()
    form.student.choices = [(s.id, s.name) for s in Student.query.all()]
    if form.validate_on_submit():
        lesson = Lesson()
        lesson.topic = form.topic.data
        lesson.student = form.student.data
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('lessons'))
    return render_template('lessons.html', form=form, students=Student.query.all(), Lesson=Lesson, lessons_active=True)


@app.route('/tutoring/payments', methods=['GET', 'POST'])
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
        return redirect(url_for('payments'))
    return render_template('payments.html', students=Student.query.all(), form=form, Payment=Payment, payments_active=True)


@app.route('/tutoring/payments/<int:payment_id>')
def payment(payment_id):
    return render_template(
        'payment.html',
        payment=Payment.query.filter_by(id=payment_id).first(),
        Student=Student,
        payments_active=True
    )
