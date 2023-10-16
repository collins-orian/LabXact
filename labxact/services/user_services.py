#!/usr/bin/env python3

"""contains services related to the user model in the app"""

# All the imports
from typing import Optional, List
from models.user_model import Users
from models import db
from . import logger


class UserService:
    """This is the userservice class that handles
    database queries"""

    def create_user(self, firstname: str, lastname: str,
                    username: str, email: str, password: str, role: str,
                    section: str) -> Users:
        """This method creates new users on the database"""
        user = Users(firstname=firstname, lastname=lastname,
                     username=username, email=email,
                     password_hash=password, role=role,
                     section=section)
        db.session.add(user)
        try:
            db.session.commit()
            logger.info(
                f'User created: {user.firstname} {user.lastname} - {user.email} - {user.username} - {user.role} - {user.section}')
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        return user

    def get_user(self, id: int) -> Users:
        """This method gets users from the
        database by id"""
        user = Users.query.get_or_404(id)
        return user

    def all_users(self) -> List[Users]:
        """This method gets all users from the
        database by the date registered"""
        users = Users.query.order_by(Users.date_added)
        return users

    def user_count(self) -> int:
        """This method counts the total no of users
        admitted"""
        count = Users.query.count()
        return count

    def get_user_by_username(self, username: str) -> Optional[Users]:
        """This method gets users from the
        database by username"""
        user = Users.query.filter_by(username=username).first()
        return user

    def get_user_by_email(self, email: str) -> Optional[Users]:
        """This method gets users from the
        database by email"""
        user = Users.query.filter_by(email=email).first()
        return user

    def update_user(self, user: Users, firstname: str, lastname: str,
                    username: str, email: str, password: str, role: str,
                    section: str) -> None:
        """This method updates users details on
        the database"""
        user.firstname = firstname
        user.lastname = lastname
        user.username = username
        user.email = email
        user.password_hash = password
        user.role = role
        user.section = section
        try:
            db.session.commit()
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        logger.info(
            f'User updated: {user.firstname} {user.lastname} - {user.email} - {user.username} - {user.role} - {user.section}')

    def delete_user(self, id: int) -> None:
        """This method deletes users details from
        the database"""
        user = self.get_user(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        logger.info(
            f'User deleted: {user.firstname} {user.lastname} - {user.email} - {user.username} - {user.role} - {user.section}')
