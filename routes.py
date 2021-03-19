from app import app, db, login_manager
from flask import render_template, redirect, url_for
from forms import CategoryForm, ExpenseForm
from models import Category, User, Expense


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    pass



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category', methods=['GET', 'POST'])
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category()
        cat.label = form.label.data
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('category'))
    return render_template("category.html", form=form, items=Category.query.all())


@app.route('/expense', methods=['GET', 'POST'])
def expense():
    form = ExpenseForm()
    form.category.choices = [(c.id, c.label) for c in Category.query.order_by('label')]
    if form.validate_on_submit():
        ex = Expense()
        ex.label = form.label.data
        ex.cost = form.cost.data
        ex.category = form.category.data
        db.session.add(ex)
        db.session.commit()
        return redirect(url_for('expense'))
    return render_template('expenses.html', form=form, items=Expense.query.all())






