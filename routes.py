from app import app, db, login_manager
from flask import render_template, redirect, url_for, Response
from forms import CategoryForm, ExpenseForm, LoginForm, StudentForm, PaymentForm, LessonForm
from models import Category, User, Expense, Student, Lesson, Payment
from flask_login import current_user, login_required, logout_user, login_user
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('error.html', title="You don't have access", photo='/static/images/not_pass.jpg')


@app.route("/nope")
@login_required
def nope():
    return render_template(
        'error.html',
        photo="/static/images/wrong.jpg",
        title="Well..."
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                           photo="/static/images/nothing.jpg",
                           photo_text="No Can Do",
                           text="Daaaamn, Looks like you have wrong Address",
                           title="No Can Do"
                           ), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            return redirect(url_for('nope'))
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


@app.route('/')
def index():
    return render_template('index.html', home=True)


@app.route('/category', methods=['GET', 'POST'])
def category():
    items = []
    if current_user.is_authenticated:
        items = Category.query.filter_by(owner=current_user.id)
    form = CategoryForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        cat = Category()
        cat.label = form.label.data
        cat.owner = current_user.id
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('category'))
    return render_template("category.html", form=form, items=items, category=True)


@app.route('/expense', methods=['GET', 'POST'])
def expense():
    form = ExpenseForm()
    ID = None
    if current_user.is_authenticated:
        ID = current_user.id
    form.category.choices = [(c.id, c.label) for c in Category.query.filter_by(owner=ID).order_by('label').all()]
    if form.validate_on_submit():
        ex = Expense()
        ex.label = form.label.data
        ex.cost = form.cost.data
        ex.category = form.category.data
        ex.user = ID
        db.session.add(ex)
        db.session.commit()
        return redirect(url_for('expense'))
    saldo = 0
    for cat in Category.query.filter_by(owner=ID).all():
        cat.summary()
        saldo += cat.month_sum
    return render_template(
        'expenses.html',
        form=form,
        items=Expense.query.filter_by(user=ID).all(),
        categories=Category.query.filter_by(owner=ID).all(),
        money=saldo,
        expense=True
    )


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
    return render_template('student.html', student=Student.query.filter_by(id=student_id).first())


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
