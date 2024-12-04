from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/account')
def account():
    return render_template("account.html")

@views.route('/appointments')
def appointments():
    return render_template("appointments.html")

@views.route('/diagnosis')
def diagnosis():
    return render_template("diagnosis.html")