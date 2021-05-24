from re import S
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

################################################################
# Registration Route
################################################################

@app.route('/') 
def index():
    return render_template("index.html")

@app.route('/register', methods =['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash("Email is already taken!")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)

    data = {
        "firstName": request.form['firstName'],
        "lastName": request.form['lastName'],
        "email": request.form['email'],
        "password": hashed_pw,
    }
    user_id = User.register_user(data)
    
    session['user_id'] = user_id
    return redirect("/dashboard")

################################
# Login Route
################################

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Credentials")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Credentials")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

################################
# Redirect to dashboard
################################

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Please Login or Register before continuing to the site!")
        return redirect('/')
    data = {
        'id': session['user_id'],
    }
    user_in_session = User.one_user(data)
    return render_template('dashboard.html', user = user_in_session)

################################
# Logout Route
################################

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')