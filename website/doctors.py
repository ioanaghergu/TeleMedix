from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Doctor, Specialization
from . import db
from sqlalchemy.orm import joinedload

doctor = Blueprint('doctor', __name__)

@doctor.route('/doctors-list', methods=['GET'])
@login_required
def get_doctors():
    doctors = Doctor.query.options(joinedload(Doctor.specialization)).all()
    return render_template("doctors_list.html", doctors=doctors, user=current_user)