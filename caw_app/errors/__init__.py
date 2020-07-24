from flask import Blueprint

errors_bp = Blueprint('errors_bp', __name__)

from caw_app.errors import handlers