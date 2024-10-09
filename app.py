import helpers
import database

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

PASSWORD_LENGTH = 5


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")
@helpers.login_required
def index():

    return render_template("index.html", grade = session["year_name"])
    


# grades enter, update, delete
@app.route("/grades")
@helpers.login_required
def grades():
    return render_template("grades.html")

@app.route("/enter_grade", methods=["POST", "GET"])
@helpers.login_required
def enter():
    if request.method == "POST":
        subject = request.form.get("subject")
        score = request.form.get("points")

        if not score or not subject:
            return helpers.apology("your input")
        
        session["year_id"] = 1
        text = "INSERT INTO scores (user_id, subject_id, score, year_id,time) VALUES ({user_id},{subject},{score},{year},CURRENT_TIMESTAMP)"
        database.insert(text.format(user_id = session["user_id"], subject = subject,score = score,year = session["year_id"]))

      
        return redirect("/")
    
    else:
        subjects = database.readData("SELECT * FROM subject")
        return render_template("enter_grade.html", subjects = subjects)

@app.route("/update_grade")
@helpers.login_required
def update_grades():
    return render_template("update_grade.html")

@app.route("/delete_grade")
@helpers.login_required
def delete_grade():
    return render_template("delete_grade.html")





# User Management Site Pages
@app.route("/register", methods = ["Post", "Get"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        username_confirm = request.form.get("username_confirm")

        rows = database.readData("SELECT * FROM users WHERE username = {username}".format(username = username))

        if not username or not username_confirm or username_confirm != username or len(rows) != 0:
            return helpers.apology("your username")
        
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        
        if not password or not password_confirm or password_confirm != password :
            return helpers.apology("your password")
        
        database.insert("INSERT INTO users (username, hash) VALUES ({username},{hash})".format(username = username, hash = generate_password_hash(password)))
        
        return redirect("/login")
    else:
        return render_template("register.html")

  
    
@app.route("/login", methods = ["POST", "GET"])
def login():

    session.clear

    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return helpers.apology("missing inputs")
        
        rows = database.readData("SELECT * FROM users WHERE username = {username}".format(username = username))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
            return helpers.apology("your password")
    
        session["user_id"] = rows[0]["user_id"]
        
        rows = database.readData("SELECT * FROM year WHERE user_id = {user_id} ORDER BY year_id DESC LIMIT 1".format(user_id = session["user_id"]))

        if len(rows) == 0 :
            return redirect("/new_year")
            
        session["year_name"] = rows[0]["year_name"]
        session["year_id"] = rows[0]["year_id"]

        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/logout")
@helpers.login_required
def logout():
    session.clear()

    return redirect("/")

@app.route("/new_year",methods = ["POST", "GET"])
@helpers.login_required
def new_year():
    if request.method == "POST":
        name = request.form.get("name")

        if not name:
            return helpers.apology("No name defined")
        database.insert("INSERT user_id, year_name INTO  year VALUES({user_id},{year_name} ))".format(user_id = session["user_id"], year_name = name))
        session["year_name"] = name
        return redirect("/")
    else:
        return render_template("new_year.html")
    

@app.route("/check_grade", methods=["POST", "GET"])
@helpers.login_required
def check_grade():
    if request.method == "POST":
        c = 1

    else:
        return render_template("/check_grade.html")