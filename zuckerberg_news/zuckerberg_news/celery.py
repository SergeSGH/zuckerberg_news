"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zuckerberg_news.settings')

app = Celery('zuckerberg_news',)

app.conf.imports = ('api.tasks',)

app.conf.beat_schedule = {
    'update ratings': {
        'task': 'api.tasks.rating_update',
        'schedule': crontab(minute='*/60')
    },
}

app.autodiscover_tasks()
