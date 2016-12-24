from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


def populate_db():
    """Populate database with needed initial data"""
    from app.models import User

    admin_user = User()
    admin_user.username = 'admin'
    admin_user.password = 'admin'

    DB.session.add(admin_user)
    DB.session.commit()
