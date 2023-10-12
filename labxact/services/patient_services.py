#!/usr/bin/env python3

"""contains services related to the patient model in the app"""

# All the imports
from models.patient_model import Patients
from models import db


class PatientService:
    """This is the patientservice class that handles
    database queries"""
    def create_patient(self, patient_id, firstname, middlename,
                       lastname, date_of_birth, age, gender, mobile,
                       email, address):
        """This method creates new patients on the database"""
        patient = Patients(patient_id, firstname, middlename,
                           lastname, date_of_birth, age, gender, mobile,
                           email, address)
        db.session.add(patient)
        db.session.commit()
        return patient

    def get_patient(self, id):
        """This method gets patients from the
        database by id"""
        patient = Patients.query.get_or_404(id)
        return patient

    def patient_count(self):
        """This method counts the total no of patients
        admitted"""
        count = Patients.query.count()
        return count

    def all_patients(self):
        """This method gets all patients from the
        database by the date registered"""
        patients = Patients.query.order_by(Patients.date_registered)
        return patients

    def get_patient_by_pid(self, pid):
        """This method gets patients from the
        database by pid"""
        patient = Patients.query.filter_by(patient_id=pid).first()
        return patient

    def update_patient(self, patient, firstname, middlename,
                       lastname, date_of_birth, age, gender, mobile,
                       email, address):
        """This method updates patients details on
        the database"""
        patient.firstname = firstname
        patient.middlename = middlename
        patient.lastname = lastname
        patient.date_of_birth = date_of_birth
        patient.age = age
        patient.gender = gender
        patient.mobile = mobile
        patient.email = email
        patient.address = address
        db.session.commit()

    def delete_patient(self, id):
        """This method deletes patients details from the database"""
        patient = self.get_patient(id)
        db.session.delete(patient)
        db.session.commit()
