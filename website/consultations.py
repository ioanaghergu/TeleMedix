from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime

consultation = Blueprint('consultation', __name__)

@consultation.route('/consultation-form', methods=['GET', 'POST'])
@login_required
def add_consultation():
    if request.method == 'POST':
        specializationId = request.form.get('specialization')
        doctorId = request.form.get('doctor')
        appointment_datetime = request.form.get('appointmentDatetime')
        notes = request.form.get('notes')

        # Convert appointment_datetime to a datetime object
        try:
            appointment_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash("Invalid date and time format", category="error")
            return redirect(url_for('consultation.add_consultation'))

        if appointment_datetime < datetime.now():
            flash("The date must be in the future", category="error")
            return redirect(url_for('consultation.add_consultation'))

        conn = current_app.db
        cursor = conn.cursor()

        existing_appointment = cursor.execute("SELECT * FROM [Appointment] WHERE [medicID] = ? AND [appointment_date] = ?", doctorId, appointment_datetime).fetchone()
        if existing_appointment:
            flash("There is already an appointment with this doctor at the same date and time", category="error")
            return redirect(url_for('consultation.add_consultation'))
        
        print(current_user.userid, doctorId, specializationId, appointment_datetime, notes)

        cursor.execute("INSERT INTO [Appointment] ([pacientID], [medicID], [appointment_date], [notes], [serviceID]) VALUES (?, ?, ?, ?, ?)", current_user.userid, doctorId, appointment_datetime, notes, 1)
        conn.commit()

        flash("Your consultation form was completed successfully", category="success")
        return redirect(url_for('views.home'))

    specializations = current_app.db.cursor().execute("SELECT * FROM [Specialization]").fetchall()
    return render_template("consultation_form.html", user=current_user, specializations=specializations)

@consultation.route('/attended-consultations', methods=['GET'])
@login_required
def get_consultations():
    conn = current_app.db
    cursor = conn.cursor()
    appointments = cursor.execute("SELECT [appointment_date], [notes], [username], [specialization_name] FROM [Appointment], [User], [Medic], [Specialization] WHERE [Appointment].[medicID] = [Medic].[medicID] AND [Medic].[medicID] = [User].[userID] AND [Medic].[specializationID] = [Specialization].[specializationID] AND [Appointment].[pacientID] = ?", current_user.userid).fetchall()
    return render_template("consultations/attended_consultations.html", appointments=appointments)