from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Home Page</h1>"

@views.route('/account')
def account():
    return "<h1>Account Page</h1>"

@views.route('/appointments')
def appointments():
    return "<h1>Appointments</h1>"

@views.route('/diagnosis')
def diagnosis():
    return "<h1>AI diagnosis page</h1>"