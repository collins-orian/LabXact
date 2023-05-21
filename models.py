#!usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50), unique=True, nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    passwd = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, passwd, role, uname, fname):
        self.uname = uname
        self.fname = fname
        self.passwd = passwd
        self.role = role
