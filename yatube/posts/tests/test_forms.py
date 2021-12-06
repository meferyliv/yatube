from django.test import Client, TestCase
from django.urls import reverse

from posts.constants import (REVERSE_CREATE_POST_URL, REVERSE_PROFILE_URL,
                             TEST_GROUP_SLUG, TEST_GROUP_TITLE, TEST_POST_TEXT,
                             TEST_USERNAME)
from posts.forms import PostForm
from posts.models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            text=TEST_POST_TEXT,
            author=User.objects.get(username=TEST_USERNAME),
            group=Group.objects.get(slug=cls.group.slug)
        )
        cls.REVERSE_POST_DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.REVERSE_POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.form = PostForm()

    def test_post_create(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Test form text',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            REVERSE_CREATE_POST_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, REVERSE_PROFILE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Test form text',
                group=self.group.pk
            ).exists()
        )

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Test form text after edit',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            self.REVERSE_POST_EDIT_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            self.REVERSE_POST_DETAIL_URL
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Test form text after edit',
                group=self.group.pk
            ).exists()
        )
