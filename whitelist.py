
from app import create_app
from app.auth.views import load_user, signup
from app.entry.views import show_entries, add_entry
from app.models import User, Entry
from manage import recreate_db
from test_all import FlaskrTestCase

create_app()
load_user(1)
signup()
User.id
User.is_valid_password('')
Entry
recreate_db()
show_entries()
add_entry()

FlaskrTestCase.setUp()
FlaskrTestCase.tearDown()
