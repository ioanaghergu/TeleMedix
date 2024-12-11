from flask import Flask
from flask_login import LoginManager
import pyodbc
from .models import User


server = 'tcp:telemedix.database.windows.net,1433'
database = 'telemedix'
username = 'telemedix'
password = 'ProiectMOPS!'
driver = '{ODBC Driver 18 for SQL Server}'  # Ensure this driver is installed

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .auth import auth
    from .generate_diagnosis import diagnosis

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(diagnosis, url_prefix='/')

    app.db = get_db_connection() 
       
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


def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        print("Database connection established")
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
