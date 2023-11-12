#!/usr/bin/env python3
"""This file contains forms for the users"""


# All required import
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import data_required, equal_to


class UserForm(FlaskForm):
    """This is the userform class used for data entry
    for the user model data"""
    firstname = StringField("First Name", validators=[data_required()])
    lastname = StringField("Last Name", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    role = SelectField(u'Role', choices=[('labstaff', 'Laboratory Staff'), ('labmanager', 'Laboratory Manager'), (
        'super', 'Supervisor'), ('admin', 'Administrator')], validators=[data_required()])
    section = SelectField(u'Assigned Section', choices=[('Reception', 'Reception'), ('Chemistry', 'Clinical Chemistry'), ('Haematology', 'Haematology'), (
        'Microbiology', 'Medical Microbiology')], validators=[data_required()])
    password = PasswordField("Password", validators=[data_required(), equal_to(
        'password_confirm', message="Passwords Must match")])
    password_confirm = PasswordField(
        "Confirm Password", validators=[data_required()])
    submit = SubmitField("Add User")


# create user form class
class UserUpdateForm(FlaskForm):
    """This class is used to update existing data
    with new data in the user model"""
    firstname = StringField("First Name", validators=[data_required()])
    lastname = StringField("Last Name", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    role = SelectField(u'Role', choices=[('labstaff', 'Laboratory Staff'), ('labmanager', 'Laboratory Manager'),
                                         ('super', 'Supervisor'), ('admin', 'Administrator')], validators=[data_required()])
    section = SelectField(u'Assigned Section', choices=[('Reception', 'Reception'),
                                                        ('Chemistry', 'Clinical Chemistry'), ('Haematology', 'Haematology'), (
        'Microbiology', 'Medical Microbiology')], validators=[data_required()])
    password = PasswordField("Password", validators=[equal_to(
        'password_confirm', message="Passwords Must match")])
    password_confirm = PasswordField(
        "Confirm Password")
    submit = SubmitField("Update User")


# Search form
class UserSearchForm(FlaskForm):
    """This class captures search details for users"""
    searched = StringField("Searched", validators=[data_required()])
    submit = SubmitField("Search")


# Login form
class LoginForm(FlaskForm):
    """This class captures login details"""
    username = StringField("Username", validators=[data_required()])
    password = PasswordField("Password", validators=[data_required()])
    submit = SubmitField("Login")
