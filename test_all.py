import unittest

from flask_testing import TestCase

from app import DB, create_app
from app.models import User


class FlaskrTestCase(TestCase):

    def create_app(self):
        app = create_app()
        DB.app = app
        self.app = app.test_client()

        DB.create_all()

        user = User('admin', 'admin')

        DB.session.add(user)
        DB.session.commit()

        return app

    def setUp(self):
        pass

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()

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
