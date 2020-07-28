from flask import Blueprint

edit_review_bp = Blueprint('edit_review_bp', __name__,url_prefix="/edit_r")

from caw_app.edit_review import routes