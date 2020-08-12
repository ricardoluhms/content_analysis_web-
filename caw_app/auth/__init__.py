## auth init file
from flask import Blueprint

auth_bp = Blueprint('auth', __name__,static_folder='auth')

from caw_app.auth import routes