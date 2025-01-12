from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .notifications import generate_one_hour_notifications


auth = Blueprint('auth', __name__)

def validateEmail(email):
    emailRegex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(emailRegex, email) 

def validatePassword(password):
    if(len(password) < 8):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmedPassword = request.form.get('confirmedPassword')
        birthDate = request.form.get('birthDate')  
        roleId = request.form.get('role')

        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [User] WHERE email = ?", email)

        user = cursor.fetchone()

        if user:
            flash("Email already exists", category="error")
        elif validateEmail(email) is None:
            flash("Invalid Email", category="error")
        elif len(name) < 7:
            flash("Name must be greater than 7 characters", category="error")
        elif validatePassword(password) is False:
            flash("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character", category="error")
        elif password != confirmedPassword:
            flash("Passwords do not match", category="error")
        else:
            hashedPassword = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO [User] (username, email, password, birth_date, roleid) VALUES (?, ?, ?, ?, ?)", name, email, hashedPassword, birthDate, roleId)
            conn.commit()

            newUser = cursor.execute("SELECT * FROM [User] WHERE email = ?", email).fetchone()
            
            if(newUser.roleID == 2): # Pacient
                cursor.execute("INSERT INTO [MedicalRecord] VALUES (?)", newUser.userID)
                conn.commit()

            activeUser = User(userid=newUser.userID,
                              email=newUser.email,
                              password=newUser.password,
                              username=newUser.username,
                              birth_date=newUser.birth_date,
                              roleid = newUser.roleID)
            
            role = cursor.execute("SELECT * FROM Role WHERE roleID = ?", roleId).fetchone()
            if role.role_name == 'DOCTOR':
                cursor.execute("INSERT INTO [Medic] (medicID) VALUES (?)", newUser.userID)
                conn.commit()
            elif role.role_name == 'PATIENT':
                cursor.execute("INSERT INTO [Pacient] (pacientID) VALUES (?)", newUser.userID)
                conn.commit()

            login_user(activeUser, remember=True)
            flash("Account created", category="success")
            return redirect(url_for('views.home'))

    roles = current_app.db.cursor().execute("SELECT * FROM Role WHERE roleID != 1").fetchall()
    return render_template("sign_up.html", user=current_user, roles=roles)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [User] WHERE email = ?", email)

        user = cursor.fetchone()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                activeUser = User(userid=user.userID,
                                  email=user.email,
                                  password=user.password,
                                  username=user.username,
                                  birth_date=user.birth_date,
                                  roleid=user.roleID)
                
                login_user(activeUser, remember=True)
                generate_one_hour_notifications()
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)

        


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


