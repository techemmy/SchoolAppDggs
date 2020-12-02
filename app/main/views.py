from . import main
from .. import create_app
from flask import (
    render_template, flash, redirect, url_for, request,
)
import os

from ..models import Alumni, Calendar, Student
from cm import Content
from ..email import send_mail

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CONT = Content()


@main.route('/')
@main.route('/<urlpath>/')
def homepage(urlpath=None):
    print(urlpath)
    return render_template("index.html")


@main.route('/classes/')
def classes():
    return render_template("classes.html")


@main.route('/courses/')
def courses():
    return render_template('courses.html')


@main.route('/calendar/')
def calendar():
    events = [[event.event,
               "{0}-{1}-{2}".format(
                   event.date.day, event.date.month, event.date.year
               )]
              for event in Calendar.query.all()]
    return render_template("calendar.html", events=events)


@main.route('/alumni/', methods=["POST", "GET"])
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


@main.route('/gallery/')
def gallery():
    return render_template("gallery.html", PICS=CONT)


@main.route('/result/')
def result():
    return render_template("results.html", R=CONT)


@main.route('/apply-admis/', methods=['GET', 'POST'])
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
                student = Student(firstname=firstname,
                                  lastname=lastname,
                                  email=email, dob=dob,
                                  gender=gender, dclass=dclass,
                                  language=language,
                                  address=address,
                                  number=number
                                  )
                student.save()

                title = "You have been Registered Successfully!"
                body = "You have registered your info successfully.\n" \
                       "To proceed with the final step of the registeration\n " \
                       "Contact any of the numbers below\n 08054738863, dggs@gmail.com"
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
                                "Number: " + str(student.number) + "\n"  \
                                "Note: Students details has also been registered " \
                                "in the database"
                send_mail(title, body, email)
                send_mail(feedback_title, feedback_body, app.config['MAIL_USERNAME'])
                flash("Registered Successfully! Check your mail or contact us "
                      "through our mail.")
        except Exception as e:
            print(e)
            flash("Network issue. If error persists please try again.")

        return redirect(url_for('.apply_admis'))

    return render_template("apply-admis.html")


@main.route('/contact/', methods=['GET', 'POST'])
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
                send_mail(title, message, app.config['MAIL_USERNAME'])
            except Exception as e:
                print(e)
                flash("Error sending mail. Check your credentials "
                      "and try again.")
                return redirect(url_for(".contact"))
            flash("The Query was sent Successfully")
            return redirect(url_for(".contact"))
        except Exception as e:
            print(e)
            flash("Network error."
                  " If error persists contact us through"
                  " our number directly.")
            return redirect(url_for(".contact"))

    return render_template("contact.html")


@main.route('/alumni-reqs/', methods=['GET', 'POST'])
def alumni_request():
    if request.method == 'POST':
        name = request.form["name"]
        year = request.form["year"]
        try:
            new_alumni = Alumni(name, year)
            new_alumni.save()
        except Exception as e:
            print(e)
            flash("Error sending request! if error persists"
                  " send your info to our mail we'll add "
                  " you.")
            return redirect(url_for('.alumni_request'))

        flash("Your request was sent successfully.")
        return redirect(url_for('.alumni_request'))
    return render_template("request-alumni.html")
