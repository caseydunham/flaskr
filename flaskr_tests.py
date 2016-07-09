import os
import unittest
import tempfile

import flaskr


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries found!' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        assert 'Login successful' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'admin')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'adminx')
        assert 'Invalid password' in rv.data

    def test_add_message(self):
        self.login('admin', 'admin')
        rv = self.app.post('/add', data=dict(
            title='<h1>Hello!</h1>',
            text='<strong>Rainy days are nice!</strong>'
        ), follow_redirects=True)
        assert 'No entries found!' not in rv.data
        assert '&lt;h1&gt;Hello!&lt;/h1&gt;' in rv.data
        assert '<strong>Rainy days are nice!</strong>' in rv.data

if __name__ == '__main__':
    unittest.main()
