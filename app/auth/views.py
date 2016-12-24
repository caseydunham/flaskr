from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import logout_user, login_user
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from werkzeug.utils import redirect

from app.auth.forms import LoginForm, SignUpForm
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
    form = LoginForm()
    if form.is_submitted():
        if form.validate():
            login_user(form.user)
            flash('Login successful')
            return redirect(url_for('entry.show_entries'))
        else:
            flash("Invalid Login")
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        DB.session.add(user)
        DB.session.commit()
        flash("User successfully created. Please login.")
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)
