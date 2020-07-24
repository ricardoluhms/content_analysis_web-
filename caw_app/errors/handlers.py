from flask import render_template, request, url_for
from caw_app import db
from caw_app.errors import errors_bp
from caw_app.api.errors import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
        print(url_for())
    return render_template(url_for("templates",filename='404.html')), 404
    #return render_template('caw_app/templates/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('caw_app/templates/500.html'), 500