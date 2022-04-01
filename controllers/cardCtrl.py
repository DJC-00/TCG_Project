from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.card import TCGCard
from flask_app.models.user import User
from functools import wraps
from threading import Thread

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user_id" in session:
            flash("Access Denied: Login Required")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/generatorHome')
def cardHome():
    return render_template('genHome.html')

@app.route('/viewCard')
def viewCard():
    if 'orientation' in session:
        orientation = session['orientation']
    else:
        orientation = ''

    imageName = session['fName']
    
    if 'cardName' in session:
        newCard = TCGCard(session['cardName'])
        session.pop('cardName')
    else:
        newCard = TCGCard()
    imgNum = TCGCard.getBg()
    
    if newCard.rarity == "Masterpiece":
        borderColor = "border-danger"
    elif newCard.rarity == "Legendary":
        borderColor = "border-success"
    elif newCard.rarity == "Rare":
        borderColor = "border-warning"
    elif newCard.rarity == "Uncommon":
        borderColor = "border-info"
    else:
        borderColor = "border-white"

    session.clear()
    return render_template('showCard.html', borderColor = borderColor, card = newCard, imageName = imageName, imgNum = imgNum, orientation = orientation)

@app.route('/login', methods=['POST'])
def user_login():
    if not User.validate_login(request.form):
        return redirect('/')
    
    query_data = {
        "email" : request.form["email"],
    }

    current_user = User.get_user_by_email(query_data)
    session["user_id"] = current_user.id
    session["user_name"] = current_user.first_name
    return redirect ('/dashboard')

@app.route('/viewCard/loading')
def loading():
    return redirect("/viewCard")