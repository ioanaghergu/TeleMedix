from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
import time, datetime

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

def validate_slots(date, startSlot, consecutiveConsultations):
    if startSlot == '' or startSlot == None:
        return False, 'Please select a start slot.'
    if consecutiveConsultations == '' or consecutiveConsultations == None:
        return False, 'Please select the number of consecutive consultations.'
    dateArr = date.split('-')
    hourArr = startSlot.split(':')
    dt = datetime.datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(hourArr[0]), int(hourArr[1]))
    if dt < datetime.datetime.now():
        return False, 'The datetime of the first availability slot must not be in the past.'
    lastSlot = dt + datetime.timedelta(minutes=int(consecutiveConsultations)*30)
    if lastSlot.date() > dt.date():
        return False, 'Consultations must be in the same day.'
    if lastSlot.hour > 20 or lastSlot.hour < 8 or dt.hour > 20 or dt.hour < 8:
        return False, 'All consultations must be between 8:00 and 20:00.'
    return True, 'Valid slots'

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
        timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()
        flash("Timetable updated.", category='success')
        return render_template("account/account.html", timetable=timetable, user=current_user, time=time)


    timetable = cursor.execute('SELECT [mon], [tue], [wed], [thu], [fri], [sat], [sun] FROM [TimeTable] WHERE [medicID] = ?', current_user.userid).fetchone()
    return render_template("doctors/timetable_form.html", timetable=timetable, user=current_user)

@doctor.route('/availability-form', methods=['GET', 'POST'])
@login_required
def availability_form():
    conn = current_app.db
    cursor = conn.cursor()
    if request.method == 'POST':
        date = request.form.get('availabilityDate')
        start_time = request.form.get('availabilityStartSlot')
        consultations = request.form.get('consecutiveConsultations')
        if validate_slots(date, start_time, consultations)[0] == False:
            flash(validate_slots(date, start_time, consultations)[1], category='error')
            return render_template("doctors/availability_form.html", user=current_user)
        ok = True
        for i in range(0, int(consultations)):
            start_slot = datetime.datetime.strptime(start_time, '%H:%M') + datetime.timedelta(minutes=i*30)
            start_date = datetime.datetime.strptime(date + ' ' + start_slot.strftime('%H:%M'), '%Y-%m-%d %H:%M')
            end_date = start_date + datetime.timedelta(minutes=30)
            same_hour_pattern = start_date.strftime('%Y-%m-%d %H:') + '00'
            previous_hour_pattern = (start_date - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:') + '00'
            next_hour_pattern = (start_date + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:') + '00'
            print(same_hour_pattern)
            same_hour = cursor.execute('SELECT [start_time], [end_time] FROM [Availability] WHERE [medicID] = ? AND ([start_time] > ? AND [start_time] < ?)', current_user.userid, previous_hour_pattern, next_hour_pattern).fetchall()
            if same_hour:
                for slot in same_hour:
                    if abs(slot.start_time - start_date) < datetime.timedelta(minutes=30):
                        ok = False
                        flash(f'Slot {start_date.time()} - {end_date.time()} overlaps with an existing slot ({slot.start_time.time()} - {slot.end_time.time()}).', category='error')
                        return render_template("doctors/availability_form.html", user=current_user)
        if ok:
            for i in range(0, int(consultations)):
                start_slot = datetime.datetime.strptime(start_time, '%H:%M') + datetime.timedelta(minutes=i*30)
                start_date = datetime.datetime.strptime(date + ' ' + start_slot.strftime('%H:%M'), '%Y-%m-%d %H:%M')
                end_date = start_date + datetime.timedelta(minutes=30)
                cursor.execute('INSERT INTO [Availability] ([date], [start_time], [end_time], [medicID], [availability_status]) VALUES (?, ?, ?, ?, ?)', datetime.datetime.strptime(date, '%Y-%m-%d'), start_date, end_date, current_user.userid, 'FREE')
                conn.commit()
    return render_template("doctors/availability_form.html", user=current_user)
