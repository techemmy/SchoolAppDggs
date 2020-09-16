from flask import Flask, render_template, request, flash
from models import *
import os
import csv
from cm import Content
from flask_mail import Mail, Message


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.urandom(25)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'emmanueltopea@gmail.com',
    MAIL_PASSWORD = ''
)
db.init_app(app)

mail = Mail(app)

CONT = Content()

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/courses/')
def courses():
    return render_template("courses.html")

@app.route('/classes/')
def classes():
    return render_template("classes.html")

@app.route('/term-dates/')
def term_dates():
    term_dates = CONT['Term-Dates']
    return render_template("term-dates.html", term_dates=term_dates)

@app.route('/alumni/', methods = ["POST", "GET"])
def alumni():
    word = request.form.get("search")
    if word is not None:
        alumni = Alumni.query.filter(
                Alumni.name.like('%{}%'.format(word.capitalize()))).all()
        return render_template("alumni.html", alumni=alumni)
    else:
        alumni = Alumni.query.all()
        return render_template("alumni.html", alumni=alumni)

@app.route('/gallery/')
def gallery():
    return render_template("gallery.html", PICS=CONT)

@app.route('/result/')
def result():
    return render_template("results.html", R=CONT)

@app.route('/apply-admis/')
def apply_admis():
    return render_template("apply-admis.html")

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        
        return render_template("submitted.html", message='The Query was sent Successfully')
    return render_template("contact.html") 

@app.route('/register/', methods=['POST'])
def register_page():
    try:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        dclass = request.form.get("class")
        language = request.form.get("languages")
        address = request.form.get("address")
        country_code = request.form.get("countrycode")
    except Exception as e:
        pass
    # Validate student's data
    if (firstname.strip() == '') or (lastname.strip() == '') \
                                 or (address.strip() == ''):
        flash("You are missing some fields!")
        return render_template("apply-admis.html") 
    else:
        try:
            student = Student.add_student(firstname=firstname, lastname=lastname, email=email, dob=dob, gender=gender, dclass=dclass, language=language, address=address, country_code=country_code)

            msg = Message("You have been Registered Successfully!",
                        sender="emmanueltopea@gmail.com",
                        recipients=[email])
            msg.body= "You have registered your info successfully\n. To proceed with the final step of the registeration\n Contact any of the numbers below\n 08054738863, dggs@gmail.com"
            mail.send(msg)
            flash("Registerd Successfully!")
        except Exception as e:
            print(e)
            message = "Check the data provided and try again... If error persists contact us!"
            return render_template("405.html", message=message) #Invalid Information Given
    return render_template("register_info.html", firstname=firstname, lastname=lastname, email=email, dob=dob, gender=gender, dclass=dclass, language=language, address=address, country_code=country_code)


@app.errorhandler(404)
def page(message):
    return render_template("404.html",)

@app.errorhandler(405)
def page(message):
    return render_template('405.html',)

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

def main():
    db.create_all()
    student = Student.query.all()
    alumni = Alumni.query.all()
    
    def update_alumni():
        if alumni == []:
            add_alumni()
        else:
            alumni_to_add = sieve_new_and_existing_alumni()
            for i in alumni_to_add:
                print(i[0], i[1])
                Alumni.add_alumni(i[0], i[1])
            
    return update_alumni

    
if __name__ == "__main__":
    with app.app_context():
        main()()
