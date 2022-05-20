
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        'е-мейл',
        help_text='е-мейл',
        unique=True
    )
    username = models.CharField(
        'Логин',
        help_text='Логин',
        max_length=20,
        unique=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class News(models.Model):
    slug = models.SlugField(
        'Заголовок транслитом',
        help_text='Заголовок транслитом',
        unique=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    title = models.CharField(
        'Заголовок',
        help_text='Заголовок',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Автор',
        help_text='Автор'
    )
    brief = models.CharField(
        'Краткое содержание',
        help_text='Краткое содержание',
        max_length=250,
    )
    contents = models.TextField(
        'Содержание',
        help_text='Содержание'
    )
    views = models.IntegerField(
        'Количество просмотров',
        help_text='Количество просмотров',
        blank=True,
        null=True

    )
    rating = models.DecimalField(
        'Рейтинг',
        help_text='Рейтинг',
        decimal_places=1,
        max_digits=2,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.slug


class IsFavorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_news',
        verbose_name='Пользователь',
        help_text='Пользователь'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='is_in_favorite',
        verbose_name='Избранная новость',
        help_text='Избранная новость'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Score(models.Model):

    scores = (
        (-1, 'negative'),
        (0, 'neutral'),
        (1, 'positive'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Пользователь',
        help_text='Пользователь'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Избранная новость',
        help_text='Избранная новость'
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Оценка',
        choices=scores,
        default=0
    )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
