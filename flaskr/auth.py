import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_required, logout_user, current_user, login_user

from . import db, login_manager
from .forms import LoginForm
from .models import User

bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('error.html', title="You don't have access", photo='/static/images/not_pass.jpg')


@bp.route("/nope")
@login_required
def nope():
    return render_template(
        'error.html',
        photo="/static/images/wrong.jpg",
        title="Well..."
    )


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                           photo="/static/images/nothing.jpg",
                           photo_text="No Can Do",
                           text="Daaaamn, Looks like you have wrong Address",
                           title="No Can Do"
                           ), 404


@bp.route('/login', methods=['GET', 'POST'])
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