#!/usr/bin/env python3

"""This contains the test cases for the user services"""

from unittest import TestCase, main

from services.user_services import UserService


class TestUserService(TestCase):
    """This class contains test cases for the user service"""

    def setUp(self) -> None:
        """This method sets up the user service for the test cases"""
        self.user_service = UserService()

    def test_create_user(self) -> None:
        """This method tests the create_user method of the user service"""
        user = self.user_service.create_user(
            "john", "doe", "johndoe", "johndoe@gmail.com", "johndoe1234", "inventory officer", "chemistry")
        self.assertEqual(user.firstname, "john")
        self.assertEqual(user.lastname, "doe")
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, "johndoe@gmail.com")
        self.assertNotEqual(user.password_hash, "johndoe1234")
        self.assertEqual(user.role, "inventory officer")
        self.assertEqual(user.section, "chemistry")

if __name__ == '__main__':
    main()
