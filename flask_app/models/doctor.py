import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models.patient import Patient
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Doctor:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.patients = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO doctors (name, email, password) VALUES (%(name)s,%(email)s,%(password)s);"
        return connectToMySQL('vet').query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM doctors WHERE email = %(email)s;"
        result = connectToMySQL('vet').query_db(query, data)
        if len(result) > 0:
            return Doctor(result[0])
        else:
            return False

    @classmethod
    def get_one_with_patients(cls, data):

        query = "SELECT * FROM doctors LEFT JOIN patients ON doctors.id = patients.doctor_id WHERE doctors.id= %(id)s;"
        results = connectToMySQL('vet').query_db(query, data)
        doctor = Doctor(results[0])
        print(doctor.patients)
        for result in results:

            temp_patient = {
                "id" : result['patients.id'],
                "name" : result['name'],
                "email" : result['email'],
                "password" : result['password'],
                "doctor_id" : result['doctor_id'],
                "created_at" : result['patients.created_at'],
                "updated_at" : result['patients.updated_at']
            }
            doctor.patients.append(Patient(temp_patient))
        print(doctor.patients)

        return doctor
        
    @staticmethod
    def validate_doctor(doctor):
        is_valid = True
        if len(doctor['name']) < 2:
            is_valid = False
            flash("Sorry, use at least 2 chars")
        if len(doctor['password']) < 8:
            is_valid = False
            flash("Sorry, use at least 8 chars")
        if not EMAIL_REGEX.match(doctor['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid