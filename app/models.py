"""SQLAlchemy models"""

from random import SystemRandom

from backports.pbkdf2 import compare_digest, pbkdf2_hmac
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import DB


class User(UserMixin, DB.Model):
    """User class for all Flaskr users"""

    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String)
    _password = DB.Column(DB.LargeBinary(120))
    _salt = DB.Column(DB.String(120))

    def __init__(self, username='', password=''):
        self.username = username

        # pylint: disable=locally-disabled,method-hidden
        self.password = password

    @hybrid_property
    def password(self):
        """Password attribute hybrid property to allow for our generated
        hashes to be used with SQLAlchemy"""

        # pylint: disable=locally-disabled,method-hidden
        return self._password

    @password.setter
    def password(self, value):
        """Hashes the password when set for later comparison
        with database hash"""
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """Checks that the given plaintext password matches
        the user's hashed password"""
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        """Hashes a plaintext password"""
        pwd = password.encode('utf-8')
        salt = bytes(self._salt)
        buff = pbkdf2_hmac('sha512', pwd, salt, iterations=10000)
        return bytes(buff)


class Entry(DB.Model):
    """Encapsulates a single Entry"""
    # pylint: disable=locally-disabled,too-few-public-methods

    __tablename__ = 'entries'

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String)
    text = DB.Column(DB.String)

    def __init__(self, title='', text=''):
        self.title = title
        self.text = text
