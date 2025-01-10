from flask import Flask
from flask_login import LoginManager
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

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')
    app.register_blueprint(diagnosis, url_prefix='/')
    app.register_blueprint(doctor, url_prefix='/')
    app.register_blueprint(consultation, url_prefix='/')

    db_instance = DatabaseConnection(
        server='tcp:tele-medix.database.windows.net,1433',
        database='telemedix',
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

    return app
