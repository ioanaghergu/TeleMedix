from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime
from .notifications import create_consultation_notification, create_cancellation_notification

consultation = Blueprint('consultation', __name__)

@consultation.route('/consultation-form', methods=['POST'])
@login_required
def add_consultation():
    doctorID = request.form.get('doctorID')
    specializationID = request.form.get('specializationID')
    print(specializationID)

    if request.method == 'POST':
        if not doctorID and not specializationID:
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

            # Add Notification
            consultation_id = cursor.execute(
                """
                SELECT TOP 1 [appointmentID] 
                FROM [Appointment] 
                WHERE [pacientID] = ? AND [medicID] = ? AND [appointment_date] = ? 
                ORDER BY [appointmentID] DESC
                """,
                (current_user.userid, doctorId, appointment_datetime)).fetchone()[0]
            create_consultation_notification(
                medic_id=doctorId,
                consultation_id=consultation_id,
                patient_name=current_user.username,
                appointment_datetime=appointment_datetime)
            
            flash("Your consultation form was completed successfully", category="success")
            return redirect(url_for('views.home'))
        else: 
            conn = current_app.db
            cursor = conn.cursor()

            # Fetch the specialization and doctor based on the IDs
            selected_specialization = cursor.execute("SELECT * FROM [Specialization] WHERE [specializationID] = ?", specializationID).fetchone()
            selected_doctor = cursor.execute("""
                SELECT m.*, u.username
                FROM [Medic] m
                JOIN [User] u ON m.medicID = u.userID
                WHERE m.medicID = ?
            """, (doctorID,)).fetchone()

            print(selected_specialization)
            print(selected_doctor)

            # If either the specialization or doctor doesn't exist, return an error
            if not selected_specialization or not selected_doctor:
                flash("Invalid specialization or doctor ID", category="error")
                return redirect(url_for('consultation.add_consultation'))

            specializations = cursor.execute("SELECT * FROM [Specialization]").fetchall()
            doctors = cursor.execute("SELECT * FROM [Medic]").fetchall()

            print(specializations)
            print(doctors)

            # Render the template with the selected specialization and doctor pre-filled
            return render_template("/consultations/consultation_form.html", 
                                user=current_user, 
                                specializations=specializations,
                                doctors=doctors,
                                selected_specialization=selected_specialization, 
                                selected_doctor=selected_doctor)

    specializations = current_app.db.cursor().execute("SELECT * FROM [Specialization]").fetchall()
    return render_template("consultation_form.html", user=current_user, specializations=specializations)

def retrieve_medic_consultations(order, user_id):
    conn = current_app.db
    cursor = conn.cursor()
    query = """
                SELECT 
                [appointmentID], 
                [appointment_date], 
                [notes], 
                [username], 
                [specialization_name],
                [Appointment].[pacientID]
            FROM 
                [Appointment]
            JOIN 
                [Pacient] ON [Appointment].[pacientID] = [Pacient].[pacientID]
            JOIN 
                [User] ON [Pacient].[pacientID] = [User].[userID]
            JOIN 
                [Medic] ON [Appointment].[medicID] = [Medic].[medicID]
            JOIN 
                [Specialization] ON [Medic].[specializationID] = [Specialization].[specializationID]
            WHERE 
                [Appointment].[medicID] = ?
            ORDER BY 
                [appointment_date] {} """.format('DESC' if order == 'desc' else 'ASC')
                
    appointments = cursor.execute(query, (user_id,)).fetchall()
    return(appointments)

@consultation.route('/my-consultations', methods=['GET'])
@login_required
def get_consultations():
    conn = current_app.db
    cursor = conn.cursor()
    
    status_filter = request.args.get('status')
    order = request.args.get('order', 'desc')
    user_id = current_user.userid
    
    if current_user.roleid == 2: # Retrieve patient's consultations  
        query = """
                SELECT 
                [appointmentID], 
                [appointment_date], 
                [notes], 
                [username], 
                [specialization_name],
                [pacientID]
            FROM 
                [Appointment]
            JOIN 
                [Medic] ON [Appointment].[medicID] = [Medic].[medicID]
            JOIN 
                [User] ON [Medic].[medicID] = [User].[userID]
            JOIN 
                [Specialization] ON [Medic].[specializationID] = [Specialization].[specializationID]
            WHERE 
                [Appointment].[pacientID] = ?
            ORDER BY 
                [appointment_date] {} """.format('DESC' if order == 'desc' else 'ASC')
                   
        appointments = cursor.execute(query, (user_id,)).fetchall() 
        
    elif current_user.roleid == 3:
        appointments = retrieve_medic_consultations(order, user_id)
    
    now = datetime.now()
    processed_appointments = []

    for appointment in appointments:
        
        # Determine status
        if appointment.appointment_date >= now and "Cancellation Reason:" not in appointment.notes:
            status = "Active"
        elif "Cancellation Reason:" in appointment.notes:
            status = "Cancelled"
        else:
            status = "Attended"

        processed_appointments.append({
            "appointmentID": appointment.appointmentID,
            "appointment_date": appointment.appointment_date,
            "notes": appointment.notes,
            "username": appointment.username,
            "specialization_name": appointment.specialization_name,
            "status": status,
            "pacientID": appointment.pacientID
        })
    
    if status_filter:
        processed_appointments = [
            appt for appt in processed_appointments if appt["status"] == status_filter
        ]
    return render_template("consultations/my_consultations.html", appointments=processed_appointments,  status_filter=status_filter, order=order)


@consultation.route('/cancel-consultation/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_consultation(appointment_id):
    cancellation_reason = request.form.get('cancellation_reason', '').strip()

    conn = current_app.db
    cursor = conn.cursor()

    # Verify the consultation belongs to the current user and is in the future
    consultation = cursor.execute(
         "SELECT [appointment_date], [notes], [medicID], [pacientID], [appointmentID] FROM [Appointment] WHERE [appointmentID] = ? AND ([pacientID] = ? OR [medicID] = ?)", 
        (appointment_id, current_user.userid, current_user.userid)).fetchone()

    if consultation:
        consultation = dict(zip([column[0] for column in cursor.description], consultation))
    else:
        flash("Consultation not found.", category="error")
        return redirect(url_for('consultation.get_consultations'))

    appointment_date = consultation['appointment_date']
    notes = consultation['notes'] or ""

    if appointment_date < datetime.now():
        flash("Cannot cancel past consultations.", category="error")
        return redirect(url_for('consultation.get_consultations'))

    #Add Notification
    medic_id = consultation['medicID']
    patient_id = consultation['pacientID']
    consultation_id = consultation['appointmentID']
    
    if current_user.userid == medic_id:
        recipient_id = patient_id
        canceler_name = f"Doctor {current_user.username}"
    elif current_user.userid == patient_id:
        recipient_id = medic_id
        canceler_name = f"Patient {current_user.username}"
    create_cancellation_notification(
        recipient_id=recipient_id,
        consultation_id=consultation_id,
        canceler_name=canceler_name,
        cancellation_reason=cancellation_reason,
        consultation_date = appointment_date)

    # Append cancellation reason to notes  
    updated_notes = f"{notes}\n\nCancellation Reason: {cancellation_reason}" if cancellation_reason else f"{notes}\n\nCancellation Reason: -"
    cursor.execute(
        "UPDATE [Appointment] SET [notes] = ? WHERE [appointmentID] = ?", 
        (updated_notes, appointment_id))
    conn.commit()
    
    flash("Consultation cancelled successfully.", category="success")
    return redirect(url_for('consultation.get_consultations'))

@consultation.route('/delete-consultation/<int:appointment_id>', methods=['POST'])
@login_required
def delete_consultation(appointment_id):
    conn = current_app.db
    cursor = conn.cursor()

    consultation = cursor.execute(
         "SELECT [appointment_date], [notes] FROM [Appointment] WHERE [appointmentID] = ? AND ([pacientID] = ? OR [medicID] = ?)", 
        (appointment_id, current_user.userid, current_user.userid)).fetchone()

    if consultation:
        consultation = dict(zip([column[0] for column in cursor.description], consultation))
    else:
        flash("Consultation not found.", category="error")
        return redirect(url_for('consultation.get_consultations'))

    appointment_date = consultation['appointment_date']
    notes = consultation['notes'] or ""

    # Check if consultation is eligible for deletion
    if appointment_date >= datetime.now() and "Cancellation Reason:" not in notes:
        flash("Only past or cancelled consultations can be deleted.", category="error")
        return redirect(url_for('consultation.get_consultations'))

    cursor.execute("DELETE FROM [Appointment] WHERE [appointmentID] = ?", (appointment_id,))
    conn.commit()

    flash("Consultation deleted successfully.", category="success")
    return redirect(url_for('consultation.get_consultations'))


@consultation.route('/edit-notes/<int:appointment_id>', methods=['POST'])
@login_required
def edit_notes(appointment_id):
    conn = current_app.db
    cursor = conn.cursor()

    appointment = cursor.execute(
        "SELECT [notes], [appointment_date], [pacientID] FROM [Appointment] WHERE [appointmentID] = ?", 
        (appointment_id,)).fetchone()
    
    if not appointment or appointment[2] != current_user.userid:
        flash("Consultation not found or you do not have permission to edit this consultation.", category="error")
        return redirect(url_for('consultation.get_consultations'))

    # Ensure status is Active
    now = datetime.now()
    if appointment.appointment_date < now or "Cancellation Reason:" in appointment.notes:
        
        flash("You can only edit notes for Active consultations.", category="error")
        return redirect(url_for('consultation.get_consultations'))


    new_notes = request.form.get('notes', '').strip()
    # Update the notes in the database
    cursor.execute(
        "UPDATE [Appointment] SET [notes] = ? WHERE [appointmentID] = ?", 
        (new_notes, appointment_id))
    conn.commit()

    flash("Notes updated successfully.", category="success")
    return redirect(url_for('consultation.get_consultations'))
