from functools import wraps
from flask import session, flash, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        flash('You need to log in.')
        return redirect(url_for('auth.admin_login'))
    return wrapper
