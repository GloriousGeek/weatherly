from flask import redirect, render_template, session
from functools import wraps

""" 
A decorator is a special type of function that can be applied to other functions 
to modify their behavior. It is designed to be used with Flask routes
"""

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function