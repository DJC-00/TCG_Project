from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.band import Band
from flask_app.models.user import User
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user_id" in session:
            flash("Access Denied: Login Required")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

