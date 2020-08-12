from flask import Blueprint

profiles_bp = Blueprint('prof', __name__, url_prefix='/prof')

from caw_app.profiles import routes