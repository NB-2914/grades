import database
import helpers

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash


def login():

    session.clear

    if  request.method == "POST":
  
        username =  request.form.get("username")
        password =  request.form.get("password")

        if not username or not password:
            return helpers.apology("missing inputs")
        text = "SELECT * FROM users WHERE username = {username}".format(username = username)
        
        rows = database.readData(text)
        return helpers.debug(rows)
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