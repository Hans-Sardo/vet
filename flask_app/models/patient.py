
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Patient:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.pet_name = data['pet_name']
        self.doctor_id = data['doctor_id']
        if 'name' in data:
            self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO patients (name, email, password, pet_name) VALUES (%(name)s,%(email)s,%(password)s,%(pet_name)s);"
        return connectToMySQL('vet').query_db(query, data)
    

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM patients WHERE id = %(id)s;"
        result = connectToMySQL('vet').query_db(query, data)
        patient = Patient(result[0])
        return patient

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM patients;"
        results = connectToMySQL('vet').query_db(query)
        print(results)
        patients = []
        for patient in results:
            patients.append(cls(patient))
        return patients

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM patients WHERE email = %(email)s;"
        result = connectToMySQL('vet').query_db(query, data)
        if len(result) > 0:
            return Patient(result[0])
        else:
            return False

    @classmethod
    def update(cls,data):
        query = "UPDATE patients SET name = %(name)s, email = %(email)s,password = %(password)s, pet_name = %(pet_name)s WHERE id = %(id)s;"
        return connectToMySQL('vet').query_db(query, data)

        
    @staticmethod
    def validate_patient(patient):
        is_valid = True
        if len(patient['name']) < 2:
            is_valid = False
            flash("Sorry, use at least 2 chars")
        if len(patient['password']) < 8:
            is_valid = False
            flash("Sorry, use at least 8 chars")
        if not EMAIL_REGEX.match(patient['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM patients WHERE id = %(id)s;"
        return connectToMySQL('vet').query_db(query, data)