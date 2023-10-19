#!/usr/bin/env python3

"""contains services related to the patient model in the app"""

# All the imports
from models.patient_model import Patients
from models import db
from typing import Optional, List
# from datetime import date
from . import logger


class PatientService:
    """This is the patientservice class that handles
    database queries"""

    def create_patient(self, patient_id: str, firstname: str, middlename: str,
                       lastname: str, date_of_birth: str, age: int, gender: str,
                       mobile: str, email: str, address: str) -> Patients:
        """This method creates new patients on the database"""
        patient = Patients(patient_id=patient_id, firstname=firstname,
                           middlename=middlename, lastname=lastname,
                           date_of_birth=date_of_birth, age=age, gender=gender,
                           mobile=mobile, email=email, address=address)
        db.session.add(patient)
        try:
            db.session.commit()
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        logger.info(
            f'Patient registered:{patient.__str__}')
        return patient

    # def calculate_age(date_of_birth: Optional[date]) -> Optional[int]:
    #     """Calculates the age of a person based on their date of birth.

    #     Args:
    #         date_of_birth: A datetime object representing the person's date of birth.

    #     Returns:
    #         An integer representing the person's age.
    #     """

    #     if date_of_birth is None:
    #         return None

    #     today = date.today()
    #     age = today.year - date_of_birth.year - \
    #         ((today.month, today.day) < (date_of_birth.month,
    #                                      date_of_birth.day))
    #     return age

    def get_patient(self, id: int) -> Patients:
        """This method gets patients from the
        database by id"""
        patient = Patients.query.get_or_404(id)
        return patient

    def patient_count(self) -> int:
        """This method counts the total no of patients
        admitted"""
        count = Patients.query.count()
        return count

    def all_patients(self) -> List[Patients]:
        """This method gets all patients from the
        database by the date registered"""
        patients = Patients.query.order_by(Patients.date_registered)
        return patients

    def get_patient_by_pid(self, pid: str) -> Optional[Patients]:
        """This method gets patients from the
        database by pid"""
        patient = Patients.query.filter_by(patient_id=pid).first()
        return patient

    def update_patient(self, patient: Patients, firstname: str, middlename: str,
                       lastname: str, date_of_birth: str, age: int, gender: str,
                       mobile: str, email: str, address: str) -> None:
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
        try:
            db.session.commit()
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        logger.info(
            f'Patient updated: {patient.__str__}')

    def delete_patient(self, id: int) -> None:
        """This method deletes patients details from the database"""
        patient = self.get_patient(id)
        db.session.delete(patient)
        try:
            db.session.commit()
        except Exception as e:
            # Handle the database error here.
            logger.error(e)
            raise e
        logger.info(
            f'Patient deleted: {patient.__str__}')
