from http import HTTPStatus

from django import forms
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.constants import (REVERSE_CREATE_POST_URL, REVERSE_FOLLOW_INDEX,
                             REVERSE_GROUP_URL, REVERSE_INDEX_URL,
                             REVERSE_PROFILE_URL, TEST_GROUP_SLUG,
                             TEST_GROUP_TITLE, TEST_IMAGE, TEST_POST_TEXT,
                             TEST_USERNAME, USER_AUTHOR)
from posts.models import Follow, Group, Post, User
from yatube.settings import PAG_VALUE


class PostPagesTest(TestCase):
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
        cls.posts_list = []
        for i in range(14):
            post = Post.objects.create(
                text=TEST_POST_TEXT,
                author=User.objects.get(username=TEST_USERNAME),
                group=Group.objects.get(slug=TEST_GROUP_SLUG),
                image=TEST_IMAGE
            )
            cls.posts_list.append(post)
        cls.post = cls.posts_list[0]
        cls.REVERSE_POST_DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.REVERSE_POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': f'{cls.post.pk}'}
        )
        cls.count = len(cls.posts_list)

    def test_pages_uses_correct_templates(self):
        template_page_names = {
            REVERSE_INDEX_URL: 'posts/index.html',
            REVERSE_GROUP_URL: 'posts/group_list.html',
            REVERSE_PROFILE_URL: 'posts/profile.html',
            self.REVERSE_POST_DETAIL_URL: 'posts/post_detail.html',
            self.REVERSE_POST_EDIT_URL: 'posts/create_post.html',
            REVERSE_CREATE_POST_URL: 'posts/create_post.html',
        }
        for reverse_name, template in template_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def tests_index_group_profile_pages(self):
        reverses_and_kwargs = {
            'index': REVERSE_INDEX_URL,
            'group': REVERSE_GROUP_URL,
            'profile': REVERSE_PROFILE_URL
        }
        for reverses in reverses_and_kwargs.values():
            response_first_page = self.guest_client.get(reverses)
            response_second_page = self.guest_client.get(reverses + '?page=2')
            first_object = response_first_page.context['page_obj'][0]
            post_text_0 = first_object.text
            post_author_0 = first_object.author.username
            post_group_0 = first_object.group.slug
            post_image_0 = first_object.image
            self.assertEqual(post_text_0, TEST_POST_TEXT)
            self.assertEqual(post_author_0, TEST_USERNAME)
            self.assertEqual(post_group_0, TEST_GROUP_SLUG)
            self.assertEqual(post_image_0, TEST_IMAGE)
            self.assertEqual(response_first_page.status_code, HTTPStatus.OK)
            self.assertEqual(response_second_page.status_code, HTTPStatus.OK)
            self.assertEqual(
                len(response_first_page.context['page_obj']),
                PAG_VALUE
            )
            self.assertEqual(
                len(response_second_page.context['page_obj']),
                self.count - PAG_VALUE
            )

    def test_post_detail_page(self):
        response = self.authorized_client.get(self.REVERSE_POST_DETAIL_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['post'].text, TEST_POST_TEXT)
        self.assertEqual(
            response.context['post'].author.username, TEST_USERNAME
        )
        self.assertEqual(
            response.context['post'].group.title, TEST_GROUP_TITLE
        )
        self.assertEqual(
            response.context['post'].image, TEST_IMAGE
        )

    def test_post_create_edit_pages(self):
        reverses_and_kwargs = {
            'post_create': REVERSE_CREATE_POST_URL,
            'post_edit': self.REVERSE_POST_EDIT_URL,
        }
        for reverses in reverses_and_kwargs.values():
            response = self.authorized_client.get(reverses)
            form_fields = {
                'text': forms.fields.CharField,
                'group': forms.fields.ChoiceField,
            }
            self.assertEquals(response.status_code, HTTPStatus.OK)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)


class PostCacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            text=TEST_POST_TEXT,
            author=User.objects.get(username=TEST_USERNAME),
        )

    def test_index_page_cache(self):
        respons_before_del = self.authorized_client.get(REVERSE_INDEX_URL)
        content_before_del = respons_before_del.content
        Post.objects.all().delete()
        response_after_del = self.authorized_client.get(REVERSE_INDEX_URL)
        content_after_del = response_after_del.content
        self.assertEqual(content_before_del, content_after_del)
        cache.clear()
        response_after_clear_cache = self.authorized_client.get(
            REVERSE_INDEX_URL
        )
        content_after_clear_cache = response_after_clear_cache.content
        self.assertNotEqual(content_before_del, content_after_clear_cache)
        self.assertNotEqual(content_after_del, content_after_clear_cache)


class PostFollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username=USER_AUTHOR)
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            text=TEST_POST_TEXT,
            author=User.objects.get(username=USER_AUTHOR),
        )
        cls.REVERSE_FOLLOW = reverse(
            'posts:profile_follow',
            kwargs={'username': f'{cls.user_author}'}
        )
        cls.REVERSE_UNFOLLOW = reverse(
            'posts:profile_unfollow',
            kwargs={'username': f'{cls.user_author}'}
        )

    def test_follow_unfollow(self):
        count_before_follow = Follow.objects.all().count()
        self.authorized_client.get(self.REVERSE_FOLLOW)
        count_after_follow = Follow.objects.all().count()
        self.assertEqual(count_after_follow, count_before_follow + 1)
        self.authorized_client.get(self.REVERSE_UNFOLLOW)
        count_after_unfollow = Follow.objects.all().count()
        self.assertEqual(count_before_follow, count_after_unfollow)

    def test_follow_index(self):
        self.authorized_client.get(self.REVERSE_FOLLOW)
        response = self.authorized_client.get(REVERSE_FOLLOW_INDEX)
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        self.assertEqual(post_text_0, TEST_POST_TEXT)
        self.assertEqual(post_author_0, USER_AUTHOR)
