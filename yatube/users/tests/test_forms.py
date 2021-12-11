from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User
from users.forms import CreationForm

from .constants import REVERSE_SIGNUP


class UserFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.form = CreationForm()

    def test_create_user(self):
        users_count = User.objects.count()
        form_data = {
            'first_name': 'testname',
            'last_name': 'testlastname',
            'username': 'testusername',
            'email': 'mefery@gmail.com',
            'password1': 'qpwoeiru',
            'password2': 'qpwoeiru',
        }
        response = self.guest_client.post(
            REVERSE_SIGNUP,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:index')
        )
        self.assertEqual(User.objects.count(), users_count + 1)
