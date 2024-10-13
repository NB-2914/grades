from flask import session, redirect, request, render_template
from functools import wraps


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    


def apology(error):
    return render_template("apology.html", error = error)

def debug(error):
    return render_template("debug.html", error = error)