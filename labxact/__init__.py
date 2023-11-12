# Imports required
from .patients.utils import PatientService
from .users.utils import UserService
from flask import Flask
from run import app
from flask_login import LoginManager
from logging import getLogger, FileHandler, Formatter, ERROR, INFO, DEBUG, WARNING
from config import Settings
from models import init_db


# Logger configurations
logger = getLogger(__name__)
# logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger.setLevel(ERROR)
logger.setLevel(INFO)

fh = FileHandler('app.log')
formatter = Formatter(
    '%(levelname)s - %(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


# App configurations
app.secret_key = Settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = Settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize services
users = UserService()
patients = PatientService()


# Database initialization
db = init_db(app)


# This handles the login features and session management for the application
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Settings):
    """This method creates the application instance"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import and register blueprints
    from main import main
    from patients import patient
    from users import user
    app.register_blueprint(main, url_prefix='/main')
    app.register_blueprint(patient, url_prefix='/patient')
    app.register_blueprint(user, url_prefix='/user')

    return app
