from django.urls import reverse

TEST_USERNAME = 'HasNoName'
TEST_POST_TEXT = 'Test text in post'
TEST_GROUP_TITLE = 'Test Group'
TEST_GROUP_SLUG = 'Test-slug'
REVERSE_INDEX_URL = reverse('posts:index')
REVERSE_GROUP_URL = reverse(
    'posts:group_list', kwargs={'slug': TEST_GROUP_SLUG}
)
REVERSE_PROFILE_URL = reverse(
    'posts:profile', kwargs={'username': TEST_USERNAME}
)
REVERSE_CREATE_POST_URL = reverse('posts:post_create')
UNEXISTING_PAGE_URL = '/unexisting_page/'
TEST_IMAGE = 'posts/1234.jpg'
USER_AUTHOR = 'Автор'
REVERSE_FOLLOW_INDEX = reverse('posts:follow_index')
TEST_COMMENT_TEXT = 'Test comment text'