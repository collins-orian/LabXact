#!/usr/bin/env python3

"""contains services related to the user model in the app"""

# All the imports
from models.user_model import Users
from models import db


class UserService:
    """This is the userservice class that handles
    database queries"""
    def create_user(self, fullname, username, email, password, role, section):
        """This method creates new users on the database"""
        user = Users(fullname=fullname, username=username, email=email,
                     password_hash=password, role=role, section=section)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, id):
        """This method gets users from the
        database by id"""
        user = Users.query.get(id)
        return user

    def all_users(self):
        """This method gets all users from the
        database by the date registered"""
        users = Users.query.order_by(Users.date_added)
        return users

    def user_count(self):
        """This method counts the total no of users
        admitted"""
        count = Users.query.count()
        return count

    def get_user_by_username(self, username):
        """This method gets users from the
        database by username"""
        user = Users.query.filter_by(username=username).first()
        return user

    def get_user_by_email(self, email):
        """This method gets users from the
        database by email"""
        user = Users.query.filter_by(email=email).first()
        return user

    def update_user(self, user, fullname, username, email, password, role, section):
        """This method updates users details on
        the database"""
        user.fullname = fullname
        user.username = username
        user.email = email
        user.password_hash = password
        user.role = role
        user.section = section
        db.session.commit()

    def delete_user(self, id):
        """This method deletes users details from
        the database"""
        user = self.get_user(id)
        db.session.delete(user)
        db.session.commit()
