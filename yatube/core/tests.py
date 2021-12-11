from http import HTTPStatus

from django.test import TestCase
from posts.tests.constants import UNEXISTING_PAGE_URL


class ViewTestClass(TestCase):
    def test_page_not_found(self):
        response = self.client.get(UNEXISTING_PAGE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
