from random import SystemRandom

from backports.pbkdf2 import compare_digest, pbkdf2_hmac
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash

from flask_login import UserMixin, LoginManager, logout_user, login_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///flaskr.db',
    SQLALCHEMY_ECHO=True,
    SECRET_KEY='development-secret-key'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode('utf-8')
        salt = bytes(self._salt)
        buff = pbkdf2_hmac('sha512', pwd, salt, iterations=10000)
        return bytes(buff)


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)


@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    entry = Entry()
    entry.title = request.form['title']
    entry.text = request.form['text']
    db.session.add(entry)
    db.session.commit()
    flash('New entry successfully added')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            user = User.query.filter(User.username == request.form['username']).one()
            if user is None:
                error = 'Invalid username'
            elif not user.is_valid_password(request.form['password']):
                error = 'Invalid password'
            else:
                login_user(user)
                flash('Login successful')
                return redirect(url_for('show_entries'))
        except (MultipleResultsFound, NoResultFound):
            error = 'Invalid username'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))


def init_db():
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    app.debug = True
    init_db()
    app.run()
