from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{8,}$')

#######################( Validation )#######################
class User:
    db = "py_exam_2_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

        self.bands = []

    @staticmethod
    def validate_registration(raw_form_data):
        is_valid = True

        if len(raw_form_data["first_name"]) < 2 or len(raw_form_data["first_name"]) > 50:
            flash("Invalid First Name: Must be at between 2 and 50 characters long")
            is_valid = False

        if len(raw_form_data["last_name"]) < 2 or len(raw_form_data["last_name"])> 50:
            flash("Invalid Last Name: Must be at between 2 and 50 characters long")
            is_valid = False

        if not User.email_validation(raw_form_data["email"]):
            is_valid = False

        if not User.password_validation(raw_form_data["password"], raw_form_data["pass_confirm"], True):
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(raw_form_data):
        isValid = True
        user_from_db = User.get_user_by_email(raw_form_data)
        if not user_from_db:
            flash("Invalid Email or Password")
            isValid = False
        elif not Bcrypt.check_password_hash(User, user_from_db.password , raw_form_data['password']):
            flash("Invalid Email or Password")
            isValid = False

        return isValid


    @staticmethod
    def email_validation(form_email):
        email_valid = True

        email_list = User.get_all_emails(form_email)

        if not EMAIL_REGEX.match(form_email):
            flash("Invalid Email: Please enter a valid Email Address")
            email_valid = False
            return email_valid

        for email in email_list:
            db_email = email['email']
            if db_email == form_email:
                flash(f"Error: Account with {form_email} already exists.")
                email_valid = False
                return email_valid
            else:
                continue

        return email_valid

    @staticmethod
    def password_validation(password, pass_confirm, reg = False):
        pass_valid = True
        if reg == True:
            if not PASS_REGEX.match(password):
                flash("Invalid Password: Password must contain at least one letter, at least one number, and be longer than eight charaters.")
                pass_valid = False
                return pass_valid

        if(password != pass_confirm):
            flash("Invalid Password: Passwords do not match")
            pass_valid = False
            return pass_valid
        return pass_valid



    @classmethod
    def create_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"""
        queryResult = connectToMySQL(cls.db).query_db(query,data)
        return queryResult

    @classmethod
    def get_all_emails(cls, form_email):
        query = ("SELECT users.email FROM users;")
        email_list = connectToMySQL(cls.db).query_db(query)
        return email_list

    @classmethod
    def get_user_by_ID(cls,data):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        if len(query_result) < 1:
            return False
        return (cls(query_result[0]))
    
    @classmethod
    def get_user_by_email(cls,data):
        query = """SELECT * FROM users WHERE email = %(email)s"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        if len(query_result) < 1:
            return False
        return (cls(query_result[0]))

    @classmethod
    def user_join_band(cls,data):
        check_query = """SELECT users.id, bands.id 
                        FROM users
                        join users_in_bands ON users.id = users_in_bands.users_id AND users_in_bands.bands_id
                        join bands ON users_in_bands.bands_id = bands.id
                        Where (users.id = "%(users_id)s") AND (bands.id = "%(bands_id)s");"""
        query_result = connectToMySQL(cls.db).query_db(check_query,data)
        if len(query_result) >= 1:
            query = """DELETE FROM users_in_bands
                    WHERE (users_id = %(users_id)s AND bands_id = %(bands_id)s);"""
            query_result = connectToMySQL(cls.db).query_db(query,data)
        elif not query_result:
            query = """insert into  users_in_bands ( users_id, bands_id )
                values (  (select users.id from users where users.id = %(users_id)s), (select bands.id from bands where bands.id = %(bands_id)s) );"""
            query_result = connectToMySQL(cls.db).query_db(query,data)
        return 

    @classmethod
    def get_user_bands_joined(cls,data):
        query = """SELECT bands_id FROM users_in_bands
        WHERE users_id = %(id)s;"""
        query_result = connectToMySQL(cls.db).query_db(query,data)
        band_array = []
        for id in query_result:
            band_array.append(id["bands_id"])
        return band_array
