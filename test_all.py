import unittest
import tempfile

from flask import Flask
from flask_testing import TestCase


from flask_login import LoginManager

from flaskr import db, User, show_entries, login, logout, add_entry


class FlaskrTestCase(TestCase):

    def create_app(self):
        self.db_fd, self.database_file = tempfile.mkstemp()

        app = Flask(__name__)
        login_manager = LoginManager()
        login_manager.login_view = 'login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

        app.add_url_rule('/', 'show_entries', show_entries)
        app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
        app.add_url_rule('/logout', 'logout', logout)
        app.add_url_rule('/add', 'add_entry', add_entry, methods=['GET', 'POST'])

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.database_file
        app.config['SECRET_KEY'] = 'super-secret-test-key'
        app.config['TESTING'] = True


        return app

    def setUp(self):
        db.create_all()

        user = User()
        user.username = 'admin'
        user.password = 'admin'
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        response = self.client.get('/')
        self.assert200(response=response)
        assert 'No entries found!' in response.data

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_successful_login_logout(self):
        rv = self.login('admin', 'admin')
        self.assert200(rv)
        assert 'Login successful' in rv.data
        rv = self.logout()
        self.assert200(rv)
        assert 'You were logged out' in rv.data

    def test_invalid_username(self):
        rv = self.login('adminx', 'admin')
        self.assert200(rv)
        assert 'Invalid username or password' in rv.data

    def test_invalid_password(self):
        rv = self.login('admin', 'adminx')
        self.assert200(rv)
        assert 'Invalid username or password' in rv.data

    def test_add_message(self):
        self.login('admin', 'admin')
        rv = self.client.post('/add', data=dict(
            title='<h1>Hello!</h1>',
            text='<strong>Rainy days are nice!</strong>'
        ), follow_redirects=True)
        self.assert200(rv)
        assert 'No entries found!' not in rv.data
        assert '&lt;h1&gt;Hello!&lt;/h1&gt;' in rv.data
        assert '&lt;strong&gt;Rainy days are nice!&lt;/strong&gt;' in rv.data

if __name__ == '__main__':
    unittest.main()
