## main init file
from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

from caw_app.main import routes