from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Specialization(db.Model):
    specialization_id = db.Column(db.Integer, primary_key=True)
    specialization_name = db.Column(db.String(150), unique=True)

class Doctor(User):
    medicId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    specializationId = db.Column(db.Integer, db.ForeignKey('specialization.specialization_id'))
    specialization = db.relationship('Specialization', backref='doctor')
    license_no = db.Column(db.String(150), unique=True)
    appointments = db.relationship('Appointment')

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.medicId'))
    doctor = db.relationship('Doctor', foreign_keys=[doctor_id])
    patient = db.relationship('User', foreign_keys=[patient_id])
    date = db.Column(db.DateTime)
    notes = db.Column(db.String(500))
    service_id = db.Column(db.Integer, nullable=True)
    availability_id = db.Column(db.Integer, nullable=True)