from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dclass = db.Column(db.String, nullable=False) 
    language = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    @staticmethod
    def add_student(firstname, lastname, email, dob,
                    gender, dclass, language, address, number):
        info = Student(firstname=firstname, lastname=lastname,
                       email=email, dob=dob, gender=gender,
                       dclass=dclass, language=language,
                       address=address, number=number)
        db.session.add(info)
        db.session.commit()


class Alumni(db.Model):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def add_alumni(name, year, confirm=False):
        alumni = Alumni(name=name, year=year)
        alumni.is_confirmed = confirm
        db.session.add(alumni)
        db.session.commit()
        
    @staticmethod
    def delete_all():
        alumnis = Alumni.query.all()
        for alumni in alumnis:
            print(alumni, 'deleted!')
            db.session.delete(alumni)
        db.session.commit()
        
    @staticmethod
    def list_all():
        all_alumni = Alumni.query.all()
        all_list = []
        for obj in all_alumni:
            all_list.append([obj.name, obj.year])
        return all_list


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwd_hash = db.Column(db.Text)

    @staticmethod
    def add_admin(username, pwd_hash):
        admin = Admin(username=username, pwd_hash=pwd_hash)
        db.session.add(admin)
        db.session.commit()


class Calendar(db.Model):
    __tablename__ = "calendar"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime)

    @staticmethod
    def add_event(event, date):
        data = Calendar(event=event, date=date)
        db.session.add(data)
        db.session.commit()
