from flask import Blueprint

manage_reviews_bp = Blueprint('mngt', __name__, url_prefix='/mngt')

from caw_app.manage_reviews import routes