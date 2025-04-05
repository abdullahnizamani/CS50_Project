from flask import redirect, render_template, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function



def is_num(s):
    return any(char.isdigit() for char in s)



def valid_extension(s):
    allowed_ext = ['jpg', 'jpeg']

    if s.split('.', 1)[1] in allowed_ext:
        return s
    else:
        return None