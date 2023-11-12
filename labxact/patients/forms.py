#!/usr/bin/env python3
"""This file contains forms for patients"""


# All required import
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import data_required


# patient registration form
class PatientRegForm(FlaskForm):
    """This is the patientregform class used for data entry
    for the patient model data"""
    patient_id = StringField("Patient ID Number (PID)",
                             validators=[data_required()])
    firstname = StringField("First Name", validators=[data_required()])
    middlename = StringField("Middle Name")
    lastname = StringField("Last Name", validators=[data_required()])
    dob = DateField("Date Of Birth", validators=[
                    data_required()], format='%Y-%m-%d')
    age = IntegerField("Age", validators=[data_required()])
    gender = SelectField("Gender", validators=[data_required()], choices=[
                         ('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    email = StringField("Email")
    mobile = StringField("Mobile", validators=[data_required()])
    address = StringField("Address", validators=[data_required()])
    submit = SubmitField("Register")


# patient update form
class PatientUpdateForm(FlaskForm):
    """This class is used to update existing data
    with new data in the patient model"""
    patient_id = StringField("Patient ID Number (PID)",
                             validators=[data_required()])
    firstname = StringField("First Name", validators=[data_required()])
    middlename = StringField("Middle Name")
    lastname = StringField("Last Name", validators=[data_required()])
    dob = DateField("Date Of Birth", validators=[
                    data_required()], format='%Y-%m-%d')
    age = IntegerField("Age", validators=[data_required()])
    gender = SelectField("Gender", validators=[data_required()], choices=[
                         ('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    email = StringField("Email")
    mobile = StringField("Mobile", validators=[data_required()])
    address = StringField("Address", validators=[data_required()])
    submit = SubmitField("Update Patient")


# Search form
class PatientSearchForm(FlaskForm):
    """This class captures search details for patients"""
    searched = StringField("Searched", validators=[data_required()])
    submit = SubmitField("Search")
