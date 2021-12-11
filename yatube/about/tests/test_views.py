from about.tests.constants import (REVERSE_ABOUT_AUTHOR_URL,
                                   REVERSE_ABOUT_TECH_URL)
from django.test import Client, TestCase


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_author_tech_pages_templates(self):
        response_author = self.guest_client.get(REVERSE_ABOUT_AUTHOR_URL)
        response_tech = self.guest_client.get(REVERSE_ABOUT_TECH_URL)
        self.assertTemplateUsed(response_author, 'about/author.html')
        self.assertTemplateUsed(response_tech, 'about/tech.html')
