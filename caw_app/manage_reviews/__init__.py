from flask import Blueprint

manage_reviews_bp = Blueprint('mgts', __name__, url_prefix='/mgts')

from caw_app.manage_reviews import routes