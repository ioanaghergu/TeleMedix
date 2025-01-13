from flask import Flask, current_app
from flask_login import LoginManager, current_user
import pyodbc
from .models import User
from .database_connection import DatabaseConnection  

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .auth import auth
    from .account import account
    from .generate_diagnosis import diagnosis
    from .doctors import doctor
    from .consultations import consultation
    from .notifications import notifications

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')
    app.register_blueprint(diagnosis, url_prefix='/')
    app.register_blueprint(doctor, url_prefix='/')
    app.register_blueprint(consultation, url_prefix='/')
    app.register_blueprint(notifications, url_prefix='/')

    db_instance = DatabaseConnection(
        server='tcp:telemedixdb.database.windows.net,1433',
        database='telemedixDB',
        username='telemedix',
        password='ProiectMOPS!',
    )
    app.db = db_instance.get_connection()

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        conn = app.db
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [User] WHERE userid = ?", id)
        user = cursor.fetchone()
        if user:
            return User(userid=user[0],
                        email=user[1],
                        password=user[2],
                        username=user[3],
                        birth_date=user[4],
                        roleid=user[5])
        return None

    @app.context_processor
    def inject_unread_count():
        if current_user.is_authenticated:
            conn = current_app.db
            cursor = conn.cursor()

            # Count unread notifications for the logged-in user
            unread_count = cursor.execute(
                "SELECT COUNT(*) FROM Notification WHERE user_id = ? AND [read] = 0",
                (current_user.userid,)).fetchone()[0]
            return {'unread_count': unread_count}
        return {'unread_count': 0}  
    return app
