# Desc: Initializes the database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """This method initializes the database and handles
    migrations of the database models"""
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
