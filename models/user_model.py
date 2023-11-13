#!usr/bin/env python3

"""Contains the user model for the app."""


# All the imports
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..labxact.extensions import db


# User Model
class Users(db.Model, UserMixin):
    """This is the user class that defines the user model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(50), nullable=False)
    section = Column(String(50), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow())

    # Relationship to the Sections table
    # section = relationship('Sections', back_populates='users')

    @property
    def password(self):
        """This method raises error if password doesn't
        match the requirement"""
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        """This method generates a hash password"""
        self.password_hash = generate_password_hash(password, "scrypt", 64)

    def veryfy_password(self, password):
        """This method matches the hash password on the database
        to that of the password entered by the user for login"""
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        """This method returns the users fullname and other details
        as string"""
        return f'{self.username} - {self.firstname} {self.lastname} - {self.email} - {self.role} - {self.section}'