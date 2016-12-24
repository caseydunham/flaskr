from flask import flash
from flask import render_template
from flask import url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.database import DB
from app.entry.forms import EntryForm
from app.models import Entry

from ..entry import entry


@entry.route('/', methods=['GET', 'POST'])
@login_required
def show_entries():
    entries = Entry.query.all()
    form = EntryForm()
    if form.validate_on_submit():
        e = Entry()
        form.populate_obj(e)

        DB.session.add(e)
        DB.session.commit()
        flash('New entry successfully added')
        return redirect(url_for('entry.show_entries'))
    return render_template('show_entries.html', entries=entries, form=form)
