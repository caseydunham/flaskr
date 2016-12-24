from app import create_app

from flask_script import Manager, Server, Shell, prompt_bool

from app.database import db, populate_db


def _make_context():
    return dict(
        app=create_app(),
        db=db
    )

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=_make_context))


@manager.command
def create_db():
    """Creates database tables and populates them."""
    db.create_all()
    populate_db()


@manager.command
def drop_db():
    """Drops database tables."""
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()