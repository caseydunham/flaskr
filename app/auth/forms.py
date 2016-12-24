from flask_wtf import FlaskForm
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app.models import User


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        try:
            user = User.query.filter_by(username=self.username.data).first()
            if user and user.is_valid_password(self.password.data):
                self.user = user
                return True
        except (MultipleResultsFound, NoResultFound):
            return False

        return False


class SignUpForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
