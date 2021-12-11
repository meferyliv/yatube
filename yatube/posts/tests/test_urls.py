from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from .constants import (REVERSE_CREATE_POST_URL, REVERSE_GROUP_URL,
                        REVERSE_INDEX_URL, REVERSE_PROFILE_URL,
                        TEST_GROUP_SLUG, TEST_GROUP_TITLE, TEST_POST_TEXT,
                        TEST_USERNAME, UNEXISTING_PAGE_URL)
from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=TEST_USERNAME)
        cls.post = Post.objects.create(
            text=TEST_POST_TEXT,
            author=cls.user,
        )
        cls.REVERSE_POST_DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.REVERSE_POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=TEST_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        response = self.guest_client.get(REVERSE_INDEX_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_create(self):
        response = self.authorized_client.get(REVERSE_CREATE_POST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_profile(self):
        response = self.guest_client.get(REVERSE_PROFILE_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_detail(self):
        response = self.guest_client.get(self.REVERSE_POST_DETAIL_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_posts_edit(self):
        response = self.authorized_client.get(self.REVERSE_POST_EDIT_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_group(self):
        response = self.guest_client.get(REVERSE_GROUP_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_unexisting_page(self):
        response = self.guest_client.get(UNEXISTING_PAGE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
