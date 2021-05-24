from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.controllers import users
from flask_bcrypt import Bcrypt
import re        
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
    

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['firstName']) < 2:
            flash('First name must be at least 2 characters long!')
            is_valid = False
        if len(data['lastName']) < 2:
            flash('Last name must be at least 2 characters long!')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email must be a valid format!')
            is_valid = False
        if len(data['email']) < 6:
            flash('Email must be at least 6 characters long!')
            is_valid = False
        if len(data['password']) < 5:
            flash('Password must be at least 5 characters long!')
            is_valid = False
        if data['password'] != data['conf_password']:
            flash('Password and confirmation password must be the same!')
            is_valid = False
        return is_valid
        

################################################################
# Query to save user to DB
################################################################


    @classmethod
    def register_user(cls, data):
        query = 'INSERT INTO users(firstName, lastName, email, password, createdAt) VALUES(%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW())'
        return connectToMySQL('loginRegistrationSchema').query_db(query, data)


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("loginRegistrationSchema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    
    @classmethod
    def one_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        only_user = connectToMySQL("loginRegistrationSchema").query_db(query, data)
        return cls(only_user[0])