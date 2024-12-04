from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def sign_up():
    return "<h1>Sign up Page</h1>"


@auth.route('/login')
def login():
    return "<h1>Login Page</h1>"


@auth.route('/logout')
def logout():
    return "<h1>Logout Page</h1>"
