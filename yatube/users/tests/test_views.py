from django.test import Client, TestCase

from .constants import REVERSE_LOGIN, REVERSE_LOGOUT, REVERSE_SIGNUP


class UsersPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_pages_uses_correct_templates(self):
        template_page_names = {
            REVERSE_LOGOUT: 'users/logged_out.html',
            REVERSE_LOGIN: 'users/login.html',
            REVERSE_SIGNUP: 'users/signup.html',
        }
        for reverse_name, template in template_page_names.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
