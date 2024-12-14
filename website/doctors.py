from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

doctor = Blueprint('doctor', __name__)

@doctor.route('/doctors-list', methods=['GET'])
@login_required
def get_doctors():
    conn = current_app.db
    cursor = conn.cursor()
    doctors = cursor.execute("SELECT [username], [specialization_name] FROM [Medic], [User], [Specialization] WHERE [User].[userID] = [Medic].[medicID] AND [Medic].[specializationID] = [Specialization].[specializationID]").fetchall()

    return render_template("doctors/doctors_list.html", doctors=doctors, user=current_user)