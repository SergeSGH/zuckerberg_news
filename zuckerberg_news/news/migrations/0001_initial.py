# Generated by Django 2.2.16 on 2022-05-19 09:40

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(help_text='е-мейл', max_length=254, unique=True, verbose_name='е-мейл')),
                ('username', models.CharField(help_text='Логин', max_length=20, unique=True, verbose_name='Логин')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Заголовок транслитом', verbose_name='Заголовок транслитом')),
                ('title', models.CharField(help_text='Заголовок', max_length=200, verbose_name='Заголовок')),
                ('brief', models.CharField(help_text='Краткое содержание', max_length=250, verbose_name='Краткое содержание')),
                ('contents', models.TextField(help_text='Содержание', verbose_name='Содержание')),
                ('views', models.IntegerField(help_text='Количество просмотров', verbose_name='Количество просмотров')),
                ('rating', models.DecimalField(decimal_places=1, help_text='Рейтинг', max_digits=2, verbose_name='Рейтинг')),
                ('author', models.ForeignKey(help_text='Автор', on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(-1, 'negative'), (0, 'neutral'), (1, 'positive')], default=0, help_text='Оценка', verbose_name='Оценка')),
                ('news', models.ForeignKey(help_text='Избранная новость', on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='news.News', verbose_name='Избранная новость')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.CreateModel(
            name='IsFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(help_text='Избранная новость', on_delete=django.db.models.deletion.CASCADE, related_name='is_in_favorite', to='news.News', verbose_name='Избранная новость')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_news', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
    ]
