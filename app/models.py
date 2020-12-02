from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

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

    def __init__(self, firstname: str, lastname: str,
                 email: str, dob: str,
                 gender: str, dclass: str,
                 language: str, address: str,
                 number: int) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dob = dob
        self.gender = gender
        self.dclass = dclass
        self.language = language
        self.address = address
        self.number = int(number)

    def save(self: object) -> None:
        db.session.add(self)
        db.session.commit()



class Alumni(db.Model):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name: str, year: int, is_confirmed: bool = False) -> None:
        self.name = name
        self.year = year
        self.is_confirmed = is_confirmed

    def save(self: object) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise e


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pwd_hash = db.Column(db.Text)

    def __init__(self, username: str, pwd: str) -> None:
        self.username = username
        self.pwd_hash = sha256_crypt.hash(pwd)

    def save(self: object) -> None:
        db.session.add(self)
        db.session.commit()


class Calendar(db.Model):
    __tablename__ = "calendar"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime)

    def __init__(self, event: str, date: str) -> None:
        self.event = event
        self.date = date

    def save(self: object) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise e
