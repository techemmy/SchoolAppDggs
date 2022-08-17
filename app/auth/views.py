from flask import (
    session, redirect, url_for, flash, request, render_template
)
from . import auth
from ..models import Admin

from passlib.hash import sha256_crypt


@auth.route('/admin-login/', methods=['POST', 'GET'])
def admin_login():
    if session.get('logged_in'):
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        admin_search = Admin.query.filter_by(username=username).first()
        if admin_search:
            if sha256_crypt.verify(pwd, admin_search.pwd_hash):
                session['logged_in'] = True
                flash("Logged {0} in successfully.".format(admin_search.username))
                return redirect(url_for('admin.index'))
            else:
                flash("Invalid Credentials.")
                return redirect(url_for('.admin_login'))
        else:
            flash("Invalid Credentials.")
            return redirect(url_for('.admin_login'))
    return render_template("admin/admin-login.html")


@auth.route('/admin-logout/')
def logout():
    session.clear()
    flash("You logged out successfully.")
    return redirect(url_for('main.homepage'))
