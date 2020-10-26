from flask import (Flask, render_template, request,
                   flash, session, url_for, redirect,
                   )
from models import db, Student, Alumni, Admin, Calendar
import os
from cm import Content
from flask_mail import Mail, Message
from functools import wraps
from passlib.hash import sha256_crypt
from collections import defaultdict

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.urandom(25)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    DEBUG=True,
    #  EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('USERNAME'),
    MAIL_PASSWORD=os.getenv('PASSWORD')
)
db.init_app(app)
mail = Mail(app)

CONT = Content()


# ------------------- FUNCTIONS ----------------------#
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            flash('You need to log in.')
            return redirect(url_for('admin_login'))
    return wrapper


def add_alumni():
    for info in CONT["Alumni"]:
        Alumni.add_alumni(info[0], info[1])


def sieve_new_and_existing_alumni():
    alumni_to_add = []
    existing_alumni = Alumni.list_all()
    for i in CONT["Alumni"]:
        if i not in existing_alumni:
            alumni_to_add.append(i)
    return alumni_to_add


def send_mail(title, body, email):
    msg = Message(title,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email])
    msg.body = body
    return mail.send(msg)

# ------------------- ROUTES ----------------- #
@app.route('/')
@app.route('/<urlpath>/')
def homepage(urlpath=None):
    print(urlpath)
    return render_template("index.html")


@app.route('/courses/')
def courses():
    return render_template("courses.html")


@app.route('/classes/')
def classes():
    return render_template("classes.html")


@app.route('/calendar/')
def calendar():
    events = [[event.event,
               f"{event.date.day}-{event.date.month}-{event.date.year}"]
              for event in Calendar.query.all()]
    return render_template("calendar.html", events=events)


@app.route('/alumni/', methods=["POST", "GET"])
def alumni():
    if request.method == 'POST':
        word = request.form.get("search")
        if word is not None:
            alumni_search = Alumni.query.filter(
                    Alumni.name.like('%{}%'.format(word.capitalize()))).all()
            search = [i for i in alumni_search if i.is_confirmed]
            return render_template("alumni.html", alumni=search,
                                   search_term=word)
        else:
            search = Alumni.query.filter_by(is_confirmed=True).all()
            return render_template("alumni.html", alumni=search)

    search = Alumni.query.filter_by(is_confirmed=True).all()
    return render_template("alumni.html", alumni=search)


@app.route('/gallery/')
def gallery():
    return render_template("gallery.html", PICS=CONT)


@app.route('/result/')
def result():
    return render_template("results.html", R=CONT)


@app.route('/apply-admis/', methods=['GET', 'POST'])
def apply_admis():
    if request.method == 'POST':
        try:
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            dob = request.form.get("dob")
            gender = request.form.get("gender")
            dclass = request.form.get("class")
            language = request.form.get("languages")
            address = request.form.get("address")
            number = request.form.get("number")
            # Validate student's data
            if (firstname.strip() == '') or (lastname.strip() == '') \
                    or (address.strip() == ''):
                flash("Invalid Information.")
                return render_template("apply-admis.html")
            else:
                student = Student.add_student(firstname=firstname,
                                              lastname=lastname,
                                              email=email, dob=dob,
                                              gender=gender, dclass=dclass,
                                              language=language,
                                              address=address,
                                              number=number)
                title = "You have been Registered Successfully!"
                body = "You have registered your info successfully\n." \
                       "To proceed with the final step of the registeration\n " \
                       "Contact any of the numbers below\n 08054738863, dggs@gmail.com"
                send_mail(title, body, email)

                feedback_title = "Student Registers"
                feedback_body = "Student Info: \n" \
                                "Firstname: " + student.firstname + "\n" \
                                "Lastname: " + student.lastname + "\n" \
                                "email: " + student.lastname + "\n" \
                                "date of birth: " + student.dob + "\n"  \
                                "gender: " + student.gender + "\n"  \
                                "Class: " + student.dclass + "\n"  \
                                "Language: " + student.language + "\n"  \
                                "Address: " + student.address + "\n"  \
                                "Number: " + student.number + "\n"  \

                send_mail(feedback_title, feedback_body, app.config['MAIL_USERNAME'])
                flash("Registerd Successfully!")
                return render_template("apply-admis.html")
        except Exception as e:
            print(e)
            flash("Network issue. If error persists please try again.")
            return redirect(url_for('apply_admis'))

    return render_template("apply-admis.html")


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            email = request.form["email"]
            subject = request.form["subject"]
            message = request.form["message"]
            title = "Query from: {0} @ {1} on {2}".format(
                name, email, subject
            )
            try:
                send_mail(title, message, app.config["MAIL_USERNAME"])
            except Exception as e:
                print(e)
                flash("Error sending mail. Check your credentials "
                      "and try again.")
                return redirect(url_for("contact"))
            flash("The Query was sent Successfully")
            return redirect(url_for(contact))
        except Exception as e:
            print(e)
            flash("Network error."
                  " If error persists contact us through"
                  " our number directly.")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route('/alumni-reqs/', methods=['GET', 'POST'])
def alumni_request():
    if request.method == 'POST':
        name = request.form["name"]
        year = request.form["year"]
        try:
            Alumni.add_alumni(name, year)
        except Exception as e:
            print(e)
            flash("Error sending request! if error persists"
                  " send your info to our mail we'll add "
                  " you.")
            return redirect(url_for('alumni_request'))

        flash("Your request was sent successfully.")
        return redirect(url_for('alumni_request'))
    return render_template("/request-alumni.html")


@app.route('/login/', methods=['POST', 'GET'])
def admin_login():
    if session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        admin_search = Admin.query.filter_by(username=username).first()
        if admin_search:
            if sha256_crypt.verify(pwd, admin_search.pwd_hash):
                session['logged_in'] = True
                flash("Logged {0} in successfully.".format(admin_search.username))
                return redirect(url_for('admin'))
            else:
                flash("Invalid Credentials.")
                return redirect(url_for('admin_login'))
        else:
            flash("Invalid Credentials.")
            return redirect(url_for('admin_login'))
    return render_template("/admin/admin-login.html")


@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    features = {"add-alumni": "Add Alumni",
                "alumni-requests": "Alumni Requests",
                "add-admin": "Add New Admin",
                "manage-calendar": "Manage Calendar"}
    return render_template("admin/admin.html", features=features)


@app.route('/admin/add-alumni', methods=['GET', 'POST'])
def add_new_alumni():
    """Page allows admin to add an alumni"""
    if request.method == 'POST':
        try:
            name = request.form["name"]
            year = request.form["year"]
            Alumni.add_alumni(name, year, True)
        except Exception as e:
            print(e)
            flash("Error adding alumni. Check data.")
            return redirect(url_for('admin'))

        flash("Added Alumni successfully.")
        return redirect(url_for('admin'))
    return render_template("admin/addAlumni.html")


@app.route('/admin/alumni-requests', methods=['GET'])
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


@app.route('/update-alumni/<int:value>/<int:pos>/')
@login_required
def update_alumni(value, pos):
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

    return redirect(url_for('admin'))


@app.route('/admin/add-admin', methods=['GET', 'POST'])
def add_new_admin():
    """Page allows admin to add new admin"""
    if request.method == 'POST':
        try:
            username = request.form["username"]
            pwd = request.form["password"]
            pwd_hash = sha256_crypt.hash(pwd)
            Admin.add_admin(username, pwd_hash)
        except Exception as e:
            print(e)
            flash("Error adding admin. Check data.")
            return redirect(url_for('admin'))

        flash("Added Admin successfully.")
        return redirect(url_for('admin'))
    return render_template("admin/addNewAdmin.html")


@app.route('/admin/manage-calendar', methods=['GET', 'POST'])
def modify_calendar():
    events = [[event.event,
               f"{event.date.day}-{event.date.month}-{event.date.year}"]
              for event in Calendar.query.all()]
    if request.method == 'POST':
        event = request.form['event']
        date = request.form['date']
        if event and date:
            Calendar.add_event(event, date)
            return redirect(url_for('admin'))
        else:
            flash("Invalid data provided!")
            return redirect(url_for('admin'))
    return render_template('admin/manageCalendar.html', dates=events)


@app.route('/del-date/<pos>/')
@login_required
def delete_event(pos):
    event = Calendar.query.get(pos)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash("Event Deleted!")
    else:
        flash("Event doesn't exists.")
    return redirect(url_for('admin'))


@app.route('/admin/logout/')
@login_required
def logout():
    session.clear()
    flash("You logged out successfully.")
    return redirect(url_for('homepage'))


@app.errorhandler(404)
def page_not_found(message):
    return render_template("error.html", message=message), 404


@app.errorhandler(405)
def invalid_request(message):
    return render_template('error.html', message=message), 405


def main():
    db.create_all()

    
if __name__ == "__main__":
    with app.app_context():
        main()
