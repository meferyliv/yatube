from http import HTTPStatus

from django.test import Client, TestCase

from .constants import REVERSE_LOGIN, REVERSE_LOGOUT, REVERSE_SIGNUP


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_users_ulrs(self):
        response_signup = self.guest_client.get(REVERSE_SIGNUP)
        response_logout = self.guest_client.get(REVERSE_LOGOUT)
        response_login = self.guest_client.get(REVERSE_LOGIN)
        self.assertEqual(response_signup.status_code, HTTPStatus.OK)
        self.assertEqual(response_logout.status_code, HTTPStatus.OK)
        self.assertEqual(response_login.status_code, HTTPStatus.OK)
