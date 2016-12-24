from flask import Flask

from app.auth import auth
from app.entry import entry
from app.database import db
from app.extensions import lm


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.config.update(dict(
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/flaskr.db',
        SQLALCHEMY_ECHO=True,
        SECRET_KEY='development-secret-key'
    ))

    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    lm.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(entry)
