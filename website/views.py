from flask import Blueprint, current_app, render_template
from flask_login import login_required, current_user
import time
from .notifications import generate_one_hour_notifications

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    generate_one_hour_notifications()
    return render_template("home.html", user=current_user)

@views.route('/account')
@login_required
def account():
    conn = current_app.db
    cursor = conn.cursor()
    timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()
    return render_template("account/account.html", user=current_user, time=time, timetable=timetable)

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
    return render_template("doctors/doctors_list.html")

@views.route('/consultation-form')
@login_required
def consultation_form():
    conn = current_app.db
    cursor = conn.cursor()
    doctors = cursor.execute("SELECT * FROM [Medic], [User], [Specialization] WHERE [User].[userID] = [Medic].[medicID] AND [Medic].[specializationID] = [Specialization].[specializationID] AND [User].[userID] <> ?", current_user.userid).fetchall()
    specializatons = cursor.execute("SELECT * FROM [Specialization]").fetchall()
    return render_template("consultations/consultation_form.html", user=current_user, doctors=doctors, specializations=specializatons)
