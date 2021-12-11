from django.test import TestCase

from .constants import (TEST_GROUP_SLUG, TEST_GROUP_TITLE, TEST_POST_TEXT,
                        TEST_USERNAME, TEST_COMMENT_TEXT, USER_AUTHOR)
from posts.models import Comment, Follow, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.author = User.objects.create_user(username=USER_AUTHOR)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_POST_TEXT
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text=TEST_COMMENT_TEXT,
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        group = PostModelTest.group
        comment = PostModelTest.comment
        expected_postobject_name = post.text[:15]
        expected_groupobject_name = group.title
        expected_commentobject_name = comment.text
        self.assertEqual(expected_postobject_name, str(post.text[:15]))
        self.assertEqual(expected_groupobject_name, str(group.title))
        self.assertEqual(expected_commentobject_name, str(comment.text))

    def test_model_follow(self):
        count_follows_before = Follow.objects.all().count()
        Follow.objects.all().delete()
        count_follows_after_del = Follow.objects.all().count()
        self.assertEqual(count_follows_after_del, count_follows_before - 1)
