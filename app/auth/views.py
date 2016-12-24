from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import logout_user, login_user
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.utils import redirect

from app.database import DB
from app.extensions import LM
from app.models import User

from ..auth import auth


@LM.user_loader
def load_user(user_id):
    """LoginManager extension load_user function"""
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            user = User.query.filter(User.username == username).one()
            if user is None:
                error = 'Invalid username or password'
            elif not user.is_valid_password(request.form['password']):
                error = 'Invalid username or password'
            else:
                login_user(user)
                flash('Login successful')
                return redirect(url_for('entry.show_entries'))
        except (MultipleResultsFound, NoResultFound, TypeError):
            error = 'Invalid username or password'
    return render_template('login.html', error=error)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        user.username = username
        user.password = password
        DB.session.add(user)
        DB.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html', error=error)
