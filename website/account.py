from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from website.models import User
from . import db
from .auth import validateEmail, validatePassword

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
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash("This email is already in use.", category='error')
            return render_template('account/edit_account.html', user=current_user)
        
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
                # Update
                current_user.name = name
                current_user.email = email
                if password:  # Only update password if provided
                    current_user.password = generate_password_hash(password, method='pbkdf2:sha256')
                db.session.commit()
                flash('Profile updated successfully!', category='success')
                return redirect(url_for('views.account'))
            except Exception as e:
                flash(f'An error occurred: {e}', category='error')

    return render_template('account/edit_account.html', user=current_user)

@account.route('/account/confirm-delete', methods=['GET'])
@login_required
def confirm_delete():
    return render_template("account/delete_account.html", user=current_user)

@account.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    
    if not password:
        flash("Password is required.", category='error')
        return redirect(url_for('account.confirm_delete'))
    
    if check_password_hash(current_user.password, password):
        db.session.delete(current_user)
        db.session.commit()
        flash("Account deleted successfully.", category="success")
        return redirect(url_for('auth.login'))
    else:
        flash("Incorrect password. Account not deleted.", category="error")
        return redirect(url_for('account.confirm_delete'))
