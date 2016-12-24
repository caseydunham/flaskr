from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.database import db
from app.models import Entry

from ..entry import entry


@entry.route('/', methods=['GET'])
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@entry.route('/add', methods=['POST'])
@login_required
def add_entry():
    e = Entry()
    e.title = request.form['title']
    e.text = request.form['text']
    db.session.add(e)
    db.session.commit()
    flash('New entry successfully added')
    return redirect(url_for('entry.show_entries'))