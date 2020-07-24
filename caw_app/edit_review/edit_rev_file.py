from flask import Blueprint, render_template
#from content_analysis_web_app.models import Edit_Reviews

edit_review_bp = Blueprint('edit_review_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='edit_rev')

@edit_review_bp.route('/')
def problem_space():
    ### to be defined
    return render_template('edit_rev_temp/00_problem_space.html')

@edit_review_bp.route('/')
def solution_space():
    ### to be defined
    return render_template('edit_rev_temp/01_solution_space.html')

@edit_review_bp.route('/')
def groups_space():
    ### to be defined
    return render_template('edit_rev_temp/02_groups_space.html')

@edit_review_bp.route('/')
def group_relation():
    ### to be defined
    return render_template('edit_rev_temp/03_group_relation.html')

@edit_review_bp.route('/')
def venn_diagram():
    ### to be defined
    return render_template('edit_rev_temp/04_venn_diagram.html')

@edit_review_bp.route('/')
def group_keywords():
    ### to be defined
    return render_template('edit_rev_temp/05_group2keywords.html')

@edit_review_bp.route('/')
def other_features():
    ### to be defined
    return render_template('edit_rev_temp/06_other_features.html')

@edit_review_bp.route('/')
def keywords_exclusions():
    ### to be defined
    return render_template('edit_rev_temp/07_keywords_exclusion.html')

@edit_review_bp.route('/')
def search_string():
    ### to be defined
    return render_template('edit_rev_temp/08_search_string.html')

@edit_review_bp.route('/')
def search_results():
    ### to be defined
    return render_template('edit_rev_temp/09_search_results.html')

@edit_review_bp.route('/')
def analysis():
    ### to be defined
    return render_template('edit_rev_temp/10_analysis.html')