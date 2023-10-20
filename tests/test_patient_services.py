#!/usr/bin/env python3

"""This contains the test cases for the patient services"""

from unittest import TestCase, main

from services.patient_services import PatientService


class TestUserService(TestCase):
    """This class contains test cases for the user service"""

    def setUp(self) -> None:
        """This method sets up the user service for the test cases"""
        self.user_service = PatientService()

    def test_create_user(self) -> None:
        """This method tests the create_user method of the user service"""
        user = self.user_service.create_patient()


if __name__ == '__main__':
    main()
