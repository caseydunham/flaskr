from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.database import DB
from app.models import Entry

from ..entry import entry


@entry.route('/', methods=['GET'])
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@entry.route('/add', methods=['POST'])
@login_required
def add_entry():
    title = request.form['title']
    text = request.form['text']

    e = Entry(title, text)

    DB.session.add(e)
    DB.session.commit()
    flash('New entry successfully added')
    return redirect(url_for('entry.show_entries'))
