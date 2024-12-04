from flask import Flask
from .views import views
from .auth import auth


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asjhxbdaeudbhsacb jasdasa'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    return app