## auth init file
from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)

from caw_app.auth import routes