from http import HTTPStatus

from django.test import Client, TestCase

from about.constants import REVERSE_ABOUT_AUTHOR_URL, REVERSE_ABOUT_TECH_URL


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_author_tech_pages(self):
        response_author = self.guest_client.get(REVERSE_ABOUT_AUTHOR_URL)
        response_tech = self.guest_client.get(REVERSE_ABOUT_TECH_URL)
        self.assertEqual(response_author.status_code, HTTPStatus.OK)
        self.assertEqual(response_tech.status_code, HTTPStatus.OK)
