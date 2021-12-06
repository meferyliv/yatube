from django.test import TestCase

from posts.constants import (TEST_GROUP_SLUG, TEST_GROUP_TITLE, TEST_POST_TEXT,
                             TEST_USERNAME)
from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_POST_TEXT
        )

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        group = PostModelTest.group
        expected_postobject_name = post.text[:15]
        expected_groupobject_name = group.title
        self.assertEqual(expected_postobject_name, str(post.text[:15]))
        self.assertEqual(expected_groupobject_name, str(group.title))
