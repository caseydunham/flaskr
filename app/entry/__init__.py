from flask import Blueprint

entry = Blueprint('entry', __name__, template_folder='templates')

import views
