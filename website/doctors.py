from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
import time

doctor = Blueprint('doctor', __name__)

def validate_interval(interval):
    if interval == '' or interval == None:
        return True, 'Unavailable'
    if interval.count(':') != 2:
        return False, "Invalid time format. Please use HH:MM-HH:MM format."
    if interval.count('-') != 1:
        return False, "Invalid time format. Please use HH:MM-HH:MM format."
    if any(char.isalpha() for char in interval):
        return False, "Invalid time format. Please use HH:MM-HH:MM format without letters."
    return True, 'Valid time format'

@doctor.route('/doctors-list', methods=['GET'])
@login_required
def get_doctors():
    conn = current_app.db
    cursor = conn.cursor()
    doctors = cursor.execute("SELECT [username], [specialization_name], [medicID] FROM [Medic] LEFT JOIN [Specialization] ON [Medic].[specializationID] = [Specialization].[specializationID] INNER JOIN [User] ON [User].[userID] = [Medic].[medicID]").fetchall()

    return render_template("doctors/doctors_list.html", doctors=doctors, user=current_user)

@doctor.route('/doctor-profile/<int:doctorid>', methods=['GET'])
@login_required
def get_doctor(doctorid):
    conn = current_app.db
    cursor = conn.cursor()
    doctor_data = cursor.execute("SELECT [username], [specialization_name], [medicID] FROM [Medic] LEFT JOIN [Specialization] ON [Medic].[specializationID] = [Specialization].[specializationID] INNER JOIN [User] ON [User].[userID] = [Medic].[medicID] WHERE [Medic].[medicID] = ?", doctorid).fetchone()
    timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', doctorid).fetchone()
    return render_template("doctors/doctor_profile.html", doctor=doctor_data, timetable=timetable, user=current_user)

@doctor.route('/get-timetable', methods=['GET'])
@login_required
def get_timetable():
    conn = current_app.db
    cursor = conn.cursor()
    timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()
    return render_template("doctors/timetable_form.html", timetable=timetable, user=current_user)

@doctor.route('/update-timetable', methods=['GET', 'POST'])
@login_required
def update_timetable():
    conn = current_app.db
    cursor = conn.cursor()
    if request.method == 'POST':
        mon = request.form.get('mon')
        tue = request.form.get('tue')
        wed = request.form.get('wed')
        thu = request.form.get('thu')
        fri = request.form.get('fri')
        sat = request.form.get('sat')
        sun = request.form.get('sun')

        timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()

        if (validate_interval(mon)[0] == False or validate_interval(tue)[0] == False or validate_interval(wed)[0] == False or validate_interval(thu)[0] == False or validate_interval(fri)[0] == False or validate_interval(sat)[0] == False or validate_interval(sun)[0] == False):
            flash("Invalid time format. Please use HH:MM-HH:MM format.", category='error')
            return render_template("doctors/timetable_form.html", timetable=timetable, user=current_user)
        
        if timetable:
            cursor.execute('UPDATE [TimeTable] SET [mon] = ?, [tue] = ?, [wed] = ?, [thu] = ?, [fri] = ?, [sat] = ?, [sun] = ? WHERE [medicID] = ?', mon, tue, wed, thu, fri, sat, sun, current_user.userid)
        else:
            cursor.execute('INSERT INTO [TimeTable] ([mon], [tue], [wed], [thu], [fri], [sat], [sun], [medicID]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', mon, tue, wed, thu, fri, sat, sun, current_user.userid)
        conn.commit()
        flash("Timetable updated.", category='success')
        return render_template("account/account.html", timetable=timetable, user=current_user, time=time)


    timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()
    return render_template("doctors/timetable_form.html", timetable=timetable, user=current_user)
