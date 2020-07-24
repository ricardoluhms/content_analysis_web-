from flask import Flask

from caw_app.api.api_file import api_bp
from caw_app.auth.auth_file import auth_bp
from caw_app.edit_review.edit_rev_file import edit_review_bp
from caw_app.manage_reviews.mngt_rev_file import manage_reviews_bp
from caw_app.general.general_file import general_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/login')
app.register_blueprint(edit_review_bp, url_prefix='/edit_review')
app.register_blueprint(manage_reviews_bp, url_prefix='/manage_reviews')
app.register_blueprint(general_bp, url_prefix='/index')
