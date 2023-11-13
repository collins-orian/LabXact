#!/usr/bin/env python3
"""This module adds extensions to the app"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
# This handles the login features and session management for the application
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    """This method loads current user based on
    the user id"""
    from models.user_model import Users
    return Users.query.get(int(user_id))


def init_db(app):
    """This method initializes the database and handles
    migrations of the database models"""
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
