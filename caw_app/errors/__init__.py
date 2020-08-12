from flask import Blueprint

errors_bp = Blueprint('errors', __name__,static_folder='errors')

from caw_app.errors import handlers