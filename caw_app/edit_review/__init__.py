from flask import Blueprint

edit_review_bp = Blueprint('edit_review_bp', __name__)

from caw_app.edit_review import routes