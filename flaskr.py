from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///flaskr.db',
    SQLALCHEMY_ECHO=True,
    SECRET_KEY='development-secret-key',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)


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
def add_entry():
    if not session.get('logged_in'):
        abort(401)
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
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run()
