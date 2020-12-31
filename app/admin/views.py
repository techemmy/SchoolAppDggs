from . import admin
from flask import (
    render_template, request, flash, redirect, url_for,
)

from ..decorators import login_required
from ..models import db, Alumni, Admin, Calendar

from collections import defaultdict
from psycopg2 import errors

features = {"add-alumni": "Add Alumni",
            "alumni-requests": "Alumni Requests",
            "add-admin": "Add New Admin",
            "manage-calendar": "Manage Calendar"}


@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ renders name and url for features """
    return render_template("admin/admin.html", features=features)


# =======================================================
# = URLS THAT USES THE FEATURES DICTIONARY KEYS AS ENDPOINTS =#
# =======================================================

# the url is from the features dict
@admin.route('/add-alumni', methods=['GET', 'POST'])
def add_new_alumni():
    """Page allows admin to add an alumni"""
    if request.method == 'POST':
        try:
            name = request.form["name"]
            year = request.form["year"]
            new_alumni = Alumni(name, year)
            new_alumni.save()
        except Exception as e:
            print(e)
            flash("Error adding alumni. Check data.")
            return redirect(url_for('.index'))

        flash("Added Alumni successfully.")
        return redirect(url_for('.index'))
    return render_template("admin/addAlumni.html")


# the url is from the features dict
@admin.route('/alumni-requests', methods=['GET'])
def accept_alumni_requests():
    """Page allows admin to accept alumni requests"""
    ref = defaultdict(int)
    confirmed_query = Alumni.query.filter_by(is_confirmed=True).all()
    requests = Alumni.query.filter_by(is_confirmed=False).all()
    not_confirmed = [[i.name, i.year] for i in requests]
    confirmed = [[i.name, i.year] for i in confirmed_query]

    for i in not_confirmed:
        if i in confirmed:
            ref[i[0]] += 1

    context = {
        "ref": ref,
        "requests": requests
    }
    return render_template("admin/alumniRequests.html",
                           context=context)


# the url is from the features dict
@admin.route('/add-admin', methods=['GET', 'POST'])
def add_new_admin():
    """Page allows admin to add new admin"""
    all_admin = Admin.query.all()
    if request.method == 'POST':
        try:
            username = request.form["username"]
            pwd = request.form["password"]
            new_admin = Admin(username, pwd)
            new_admin.save()
            flash("Added Admin successfully.")
        except errors.UniqueViolation:
            flash("Admin with username already exists.")
        except Exception as e:
            print(type(e), dir(e))
            flash("Error adding admin. Check data.")
        return redirect(url_for('.index'))
    return render_template("admin/addNewAdmin.html", admins=all_admin)


# the url is from the features dict
@admin.route('/manage-calendar', methods=['GET', 'POST'])
def modify_calendar():
    events = [[event.event,
               "{0}-{1}-{2}".format(
                   event.date.day, event.date.month, event.date.year
               )]
              for event in Calendar.query.all()]
    if request.method == 'POST':
        event = request.form['event']
        date = request.form['date']
        if event and date:
            new_cal = Calendar(event, date)
            new_cal.save()
            flash("Date added successfully.")
        else:
            flash("Invalid data provided!")
        return redirect(url_for('.index'))
    return render_template('admin/manageCalendar.html', dates=events)


# ============================================
# = URL THAT USES FEATURES DICT ENDS HERE = #
# ============================================

# =============================================
# = ACTION LINKS FROM ADMIN PAGE =#
# =============================================

@admin.route('/update-alumni/<int:value>/<int:pos>/')
@login_required
def update_alumni(value: int, pos: int) -> None:
    alumni_act = Alumni.query.get(pos)
    if alumni_act:
        if value:
            alumni_act.is_confirmed = value
            db.session.commit()
            print(value, alumni_act, alumni_act.is_confirmed)
            flash("Alumni added successfully.")
        else:
            db.session.delete(alumni_act)
            db.session.commit()
            print(value, alumni_act, alumni_act.is_confirmed)
            flash("Alumni deleted successfully.")
    else:
        flash("Alumni does not exists anymore.")

    return redirect(url_for('.index'))


@admin.route('/del-date/<pos>/')
@login_required
def delete_event(pos: int):
    event = Calendar.query.get(pos)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash("Event Deleted!")
    else:
        flash("Event doesn't exists.")
    return redirect(url_for('.index'))
