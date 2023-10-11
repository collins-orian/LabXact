#!/usr/bin/env python3

"""contains services related to the patient model in the app"""

# All the imports
from models.patient_model import Patients
from models import db


class PatientService:
    def create_patient(self, patient_id, firstname, middlename,
                       lastname, date_of_birth, age, gender, mobile,
                       email, address):
        patient = Patients(patient_id, firstname, middlename,
                           lastname, date_of_birth, age, gender, mobile,
                           email, address)
        db.session.add(patient)
        db.session.commit()
        return patient

    def get_patient(self, id):
        patient = Patients.query.get_or_404(id)
        return patient

    def patient_count(self):
        count = Patients.query.count()
        return count

    def all_patients(self):
        patients = Patients.query.order_by(Patients.date_registered)
        return patients

    def get_patient_by_pid(self, pid):
        patient = Patients.query.filter_by(patient_id=pid).first()
        return patient

    def update_patient(self, patient, firstname, middlename,
                       lastname, date_of_birth, age, gender, mobile,
                       email, address):
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
        patient = self.get_patient(id)
        db.session.delete(patient)
        db.session.commit()
