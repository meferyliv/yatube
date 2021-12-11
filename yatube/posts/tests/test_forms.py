import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .constants import (REVERSE_CREATE_POST_URL, REVERSE_PROFILE_URL,
                        TEST_GROUP_SLUG, TEST_GROUP_TITLE, TEST_POST_TEXT,
                        TEST_USERNAME)
from posts.forms import CommentForm, PostForm
from posts.models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
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
        cls.REVERSE_COMMENT_URL = reverse(
            'posts:add_comment', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.REVERSE_ON_LOGIN = (
            (reverse('users:login')
             + f'?next=%2Fposts%2F{cls.post.pk}%2Fcomment')
        )
        cls.form = PostForm()
        cls.form_comment = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_create(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Test form text',
            'group': self.group.pk,
            'author': self.user,
            'image': uploaded
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
                group=self.group.pk,
                author=self.user,
                image=f'posts/{uploaded}'
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

    def test_comment(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Test comment',
        }
        response_guest = self.guest_client.get(self.REVERSE_COMMENT_URL)
        self.assertEqual(response_guest.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response_guest, self.REVERSE_ON_LOGIN)
        response_user = self.authorized_client.post(
            self.REVERSE_COMMENT_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response_user,
            self.REVERSE_POST_DETAIL_URL
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text='Test comment',
            ).exists()
        )
