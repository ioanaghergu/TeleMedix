from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/account')
def account():
    return render_template("account.html")

@views.route('/appointments')
def appointments():
    return render_template("appointments.html")

@views.route('/diagnosis')
def diagnosis():
    return render_template("diagnosis.html")