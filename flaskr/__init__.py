from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///myDB.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )
    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():

        from . import auth, money, tutoring
        app.register_blueprint(auth.bp)
        app.register_blueprint(money.bp)
        app.register_blueprint(tutoring.bp)

    app.debug = True
    return app
