from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from website.models import User
from . import database as db
from .auth import validateEmail, validatePassword
import time

account = Blueprint('account', __name__)

@account.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation for the fields
        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [User] WHERE email = ?", email)

        existing_user = cursor.fetchone()
        print(current_user.userid)

        if existing_user and existing_user.userID != current_user.userid:
            flash("This email is already in use.", category='error')
            return render_template('account/edit_account.html', user=current_user, time=time)
        
        if not name or len(name) < 7:
            flash("Name must be at least 7 characters long.", category='error')
        elif not validateEmail(email):
            flash("Invalid email format.", category='error')
        elif password and not validatePassword(password):
            flash("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character", category='error')
        elif password and password != confirm_password:
            flash("Passwords do not match.", category='error')
        else:
            try:
                if password:  # Only update password if provided
                    newPassword = generate_password_hash(password, method='pbkdf2:sha256')
                    cursor.execute("UPDATE [User] SET username = ?, email = ?, password = ? WHERE userID = ?", name, email, newPassword, current_user.userid)
                else:
                    cursor.execute("UPDATE [User] SET username = ?, email = ? WHERE userID = ?", name, email, current_user.userid)
                
                conn.commit()

                updatedUser = cursor.execute("SELECT * FROM [User] WHERE userID = ?", current_user.userid).fetchone()
                
                activeUser = User(userid=updatedUser.userID,
                              email=updatedUser.email,
                              password=updatedUser.password,
                              username=updatedUser.username,
                              birth_date=updatedUser.birth_date,
                              roleid =updatedUser.roleID)
                
                login_user(activeUser, remember=True)
                flash('Profile updated successfully!', category='success')
                return redirect(url_for('views.account'))
            except Exception as e:
                flash(f'An error occurred: {e}', category='error')

    return render_template('account/edit_account.html', user=current_user, time=time)

@account.route('/account/confirm-delete', methods=['GET'])
@login_required
def confirm_delete():
    return render_template("account/delete_account.html", user=current_user, time=time)

@account.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    
    if not password:
        flash("Password is required.", category='error')
        return redirect(url_for('account.confirm_delete'))
    
    if check_password_hash(current_user.password, password):
        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("DELETE FROM [User] WHERE userID = ?", current_user.userid)
        conn.commit()
        logout_user()
        flash("Account deleted successfully.", category="success")
        return redirect(url_for('auth.login'))
    else:
        flash("Incorrect password. Account not deleted.", category="error")
        return redirect(url_for('account.confirm_delete'))
