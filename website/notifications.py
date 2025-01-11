from datetime import datetime, timedelta
from flask import current_app, flash, redirect, render_template, Blueprint, url_for
from flask_login import current_user, login_required

notifications = Blueprint('notifications', __name__)

def generate_one_hour_notifications():
    conn = current_app.db
    cursor = conn.cursor()

    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)
    
    consultations = cursor.execute(
        """
        SELECT appointmentID, medicID, pacientID, appointment_date 
        FROM Appointment 
        WHERE appointment_date BETWEEN ? AND ? 
        AND (notes NOT LIKE '%Cancellation Reason:%' OR notes IS NULL)
        """,
        (now, one_hour_later)).fetchall()
    
    for consultation in consultations:
        consultation_pacientID = consultation[2]
        consultation_medicID = consultation[1]
        for user_id in [consultation_pacientID, consultation_medicID]:
            existing_notification = cursor.execute(
                """
                SELECT id 
                FROM Notification 
                WHERE consultation_id = ? AND user_id = ? AND type = 'one_hour'
                """,
                (consultation.appointmentID, user_id)).fetchone()

            if not existing_notification:
                if user_id == consultation_pacientID:
                    message = f"Reminder: Your consultation is scheduled at {consultation.appointment_date}."
                else:
                    message = f"Reminder: You have a consultation with a patient at {consultation.appointment_date}."

                cursor.execute(
                    """
                    INSERT INTO Notification (user_id, consultation_id, message, type) 
                    VALUES (?, ?, ?, 'one_hour')
                    """,
                    (user_id, consultation.appointmentID, message))
    conn.commit()

@notifications.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    conn = current_app.db
    cursor = conn.cursor()

    notifications = cursor.execute(
        """
        SELECT id, message, [read], created_at 
        FROM Notification 
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (current_user.userid,)).fetchall()

    unread_count = sum(1 for n in notifications if not n.read)

    notification_list = [
        {
            "id": n.id,
            "message": n.message,
            "read": n.read,
            "created_at": n.created_at,
        }
        for n in notifications]

    return render_template('/notifications/notifications.html', notifications=notification_list,unread_count=unread_count)

@notifications.route('/notifications/mark-as-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_as_read(notification_id):
    conn = current_app.db
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Notification SET [read] = 1 WHERE id = ? AND user_id = ?",
        (notification_id, current_user.userid))
    conn.commit()

    flash("Notification marked as read.", category="success")
    return redirect(url_for('notifications.get_notifications'))

@notifications.route('/notifications/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    conn = current_app.db
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Notification WHERE id = ? AND user_id = ? AND [read] = 1",
        (notification_id, current_user.userid))
    conn.commit()

    flash("Notification deleted.", category="success")
    return redirect(url_for('notifications.get_notifications'))

