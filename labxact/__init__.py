# Imports required
from flask import Flask
from .extensions import login_manager
from .config import settings
from .extensions import init_db


def create_app(config_class=settings):
    """This method creates the application instance"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    # App configurations
    app.secret_key = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from .main import main
    from .patients import patient
    from .users import user
    app.register_blueprint(main, url_prefix='/main')
    app.register_blueprint(patient, url_prefix='/patient')
    app.register_blueprint(user, url_prefix='/user')

    return app
