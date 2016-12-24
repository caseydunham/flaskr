from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def populate_db():
    from app.models import User

    admin_user = User()
    admin_user.username = 'admin'
    admin_user.password = 'admin'

    db.session.add(admin_user)
    db.session.commit()
