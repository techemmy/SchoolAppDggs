from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message=e), 404


@main.app_errorhandler(405)
def invalid_request(e):
    return render_template('error.html', message=e), 405


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', message=e), 500
