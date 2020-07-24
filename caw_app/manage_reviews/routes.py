from flask import render_template
from caw_app.manage_reviews import manage_reviews_bp
from caw_app.models import Manage_Reviews

@manage_reviews_bp.route('/')
def manage_screen():
    ### to be defined
    return render_template('mngt_rev_temp/manage_screen.html')

@manage_reviews_bp.route('/')
def new_review():
    ### to be defined
    return render_template('mngt_rev_temp/new_review.html')

@manage_reviews_bp.route('/')
def load_review():
    ### to be defined
    return render_template('mngt_rev_temp/load_review.html')

@manage_reviews_bp.route('/')
def share_review():
    ### to be defined
    return render_template('mngt_rev_temp/share_review.html')

""" Code example
# @products_bp.route('/view/<int:product_id>')
# def view(product_id):
#     product = Product.query.get(product_id)
#     return render_template('products/view.html', product=product) """