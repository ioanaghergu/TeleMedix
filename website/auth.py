from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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
        role_id = request.form.get('role')

        print(role_id)
        user = User.query.filter_by(email = email).first()

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
            newUser = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), role_id=role_id)
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash("Account created", category="success")
            return redirect(url_for('views.home'))
        
    roles = Role.query.filter(Role.id != 1).all()

    return render_template("sign_up.html", user=current_user, roles=roles)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
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


