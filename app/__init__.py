"""
__init__.py
Flaskr App Module
"""

from flask import Flask

from app.auth import auth
from app.entry import entry
from app.database import DB
from app.extensions import LM


__title__ = "flaskr"
__version__ = "1.0.0"


def create_app():
    """Configures and creates the flaskr application"""
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
    """Registers flask extensions on the app module"""
    DB.init_app(app)
    LM.init_app(app)


def register_blueprints(app):
    """Registers blueprints on the app module"""
    app.register_blueprint(auth)
    app.register_blueprint(entry)
