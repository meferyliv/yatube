from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q

User = get_user_model()


class Post(models.Model):
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts_group',
        verbose_name='Сообщество'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]


class Group(models.Model):
    title = models.CharField('Название сообщества', max_length=200)
    slug = models.SlugField('Адрес в URL - group/', unique=True)
    description = models.TextField('Описание сообщества')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ('-title',)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("author",)
        constraints = (
            models.CheckConstraint(
                check=~Q(user=F('author')), name='user_author_can_not_be_equal'
            ),
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_follow'
            ),
        )

    def __str__(self):
        return f"{self.user} подписан на автора {self.author}"
