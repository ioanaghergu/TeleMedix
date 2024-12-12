from flask import Blueprint, render_template
from flask_login import login_required, current_user
import time
from sqlalchemy.orm import joinedload

from website.models import Doctor, Specialization

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/account')
@login_required
def account():
    return render_template("account/account.html", user=current_user, time=time)

@views.route('/appointments')
@login_required
def appointments():
    return render_template("appointments.html", user=current_user)

@views.route('/diagnosis')
def diagnosis():
    return render_template("diagnosis.html")

@views.route('/doctors')
@login_required
def doctors_list():
    return render_template("doctors_list.html")

@views.route('/consultation-form')
@login_required
def consultation_form():
    doctors = Doctor.query.options(joinedload(Doctor.specialization)).all()
    specializatons = Specialization.query.all()
    return render_template("consultation_form.html", user=current_user, doctors=doctors, specializations=specializatons)
