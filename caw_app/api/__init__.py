## init api file
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from caw_app.api import users, errors, tokens