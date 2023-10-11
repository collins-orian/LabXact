#!/usr/bin/env python3

"""contains services related to the user model in the app"""

# All the imports
from models.user_model import Users
from models import db


class UserService:
    def create_user(self, fullname, username, email, password, role, section):
        user = Users(fullname=fullname, username=username, email=email,
                     password_hash=password, role=role, section=section)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, id):
        user = Users.query.get(id)
        return user

    def all_users(self):
        users = Users.query.order_by(Users.date_added)
        return users

    def user_count(self):
        count = Users.query.count()
        return count

    def get_user_by_username(self, username):
        user = Users.query.filter_by(username=username).first()
        return user

    def get_user_by_email(self, email):
        user = Users.query.filter_by(email=email).first()
        return user

    def update_user(self, user, fullname, username, email, password, role, section):
        user.fullname = fullname
        user.username = username
        user.email = email
        user.password_hash = password
        user.role = role
        user.section = section
        db.session.commit()

    def delete_user(self, id):
        user = self.get_user(id)
        db.session.delete(user)
        db.session.commit()
