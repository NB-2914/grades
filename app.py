import helpers


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQL("sqlite:///grades.db")

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
        
        db.execute("INSERT INTO scores (user_id, subject_id, score, year_id,time) VALUES (?,?,?,?,CURRENT_TIMESTAMP)", session["user_id"], subject, score, session["year_id"])
        
        return redirect("/")
    
    else:
        subjects = db.execute("SELECT * FROM subjects")
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
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not username or not username_confirm or username_confirm != username or len(rows) != 0:
            return helpers.apology("your username")
        
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        
        if not password or not password_confirm or password_confirm != password :
            return helpers.apology("your password")
        
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))
        
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
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
            return helpers.apology("your password")
    
        session["user_id"] = rows[0]["user_id"]
        
        rows = db.execute("SELECT * FROM year WHERE user_id = ? ORDER BY year_id DESC LIMIT 1", session["user_id"])
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