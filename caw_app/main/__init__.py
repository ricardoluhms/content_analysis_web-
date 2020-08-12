## main init file
from flask import Blueprint

main_bp = Blueprint('main', __name__, static_folder='main')

from caw_app.main import routes