import io

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)
from flask_login import current_user
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .forms import CategoryForm, ExpenseForm
from .models import Category, Expense, User
from . import db

bp = Blueprint('money', __name__)


@bp.route('/')
def index():
    return render_template('index.html', home=True)


@bp.route('/category', methods=['GET', 'POST'])
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
        return redirect(url_for('money.category'))
    return render_template("category.html", form=form, items=items, category=True)


@bp.route('/expense', methods=['GET', 'POST'])
def expense():
    form = ExpenseForm()
    ID = None
    if current_user.is_authenticated:
        ID = current_user.id
    form.category.choices = [(c.id, c.label) for c in Category.query.filter_by(owner=ID).order_by('label').all()]
    form.split_with.choices = [(u.id, u.username) for u in User.query.all()]
    if form.validate_on_submit():
        ex = Expense()
        ex.label = form.label.data
        ex.cost = form.cost.data
        ex.category = form.category.data
        ex.user = ID
        db.session.add(ex)
        db.session.commit()
        return redirect(url_for('money.expense'))
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


@bp.route('/plot.png')
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
