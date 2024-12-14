from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userid, email, password, username, birth_date, roleid):
        self.userid = userid
        self.email = email
        self.password = password
        self.username = username
        self.birth_date = birth_date
        self.roleid = roleid

    def get_id(self):
        return self.userid
    

class Specialization():
    def __init__(self, specializationid, specialization_name):
        self.specializationid = specializationid
        self.specialization_name = specialization_name

    def get_id(self):
        return self.specializationid
    
class Service():
    def __init__(self, serviceid, service_name, specializationid):
        self.serviceid = serviceid
        self.service_name = service_name
        self.specializationid = specializationid

    def get_id(self):
        return self.serviceid
    

class Medic():
    def __init__(self, medicid, specializationid, licence_no):
        self.medicid = medicid
        self.specializationid = specializationid
        self.licence_no = licence_no

    def get_id(self):
        return self.medicid
    
class Appointment():
    def __init__(self, appointmentid, patientid, medicid, appointment_date, availabilityid, serviceid, notes, specializationid):
        self.appointmentid = appointmentid
        self.patientid = patientid
        self.medicid = medicid
        self.appointment_date = appointment_date
        self.availabilityid = availabilityid
        self.serviceid = serviceid
        self.notes = notes
        self.specializationid = specializationid

    def get_id(self):
        return self.appointmentid

