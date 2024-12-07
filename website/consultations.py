from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .models import Doctor, Specialization, Appointment
from . import db
from datetime import datetime

consultation = Blueprint('consultation', __name__)

@consultation.route('/consultation-form', methods=['GET', 'POST'])
def add_consultation():
    if request.method == 'POST':
        patient_id = current_user.id
        specialization_id = request.form.get('specialization')
        doctor_id = request.form.get('doctor')
        date = request.form.get('date')
        time = request.form.get('time')
        notes = request.form.get('notes')

        if not specialization_id or not doctor_id or not date:
            flash("All fields are required", category="error")
            return redirect(url_for('consultation.add_consultation'))
        try:
            appointment_date = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        except ValueError:
            flash("Invalid date format", category="error")
            return redirect(url_for('consultation.add_consultation'))

        if appointment_date < datetime.now():
            flash("The date must be in the future", category="error")
            return redirect(url_for('consultation.add_consultation'))

        existing_appointment = Appointment.query.filter_by(doctor_id=doctor_id, date=appointment_date).first()
        if existing_appointment:
            flash("There is already an appointment with this doctor at the same date and time", category="error")
            return redirect(url_for('consultation.add_consultation'))

        newAppointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=appointment_date, notes=notes)
        db.session.add(newAppointment)
        db.session.commit()
        flash("Your consultation form was completed successfully", category="success")
        return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)



