from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

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
    country_code = db.Column(db.String, nullable=False)

    def add_student(firstname, lastname, email, dob, gender, dclass, language, address, country_code):
        info = Student(firstname=firstname, lastname=lastname, email=email, dob=dob, gender=gender, dclass=dclass, language=language, address=address, country_code=country_code)
        db.session.add(info)
        db.session.commit()

class Alumni(db.Model):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

    def add_alumni(name, year):
        alumni = Alumni(name=name, year=year)
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

