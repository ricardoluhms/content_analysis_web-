from flask import Blueprint

manage_reviews_bp = Blueprint('manage_reviews_bp', __name__,
                                template_folder='templates',
                                static_folder='static', 
                                static_url_path='mngt_revs')

from caw_app.manage_reviews import routes