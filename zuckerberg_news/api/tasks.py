from django.db.models import Avg

from news.models import News
from zuckerberg_news.celery import app


@app.task
def rating_update():
    news_list = News.objects.all().annotate(avg_score=Avg('scores__score'))
    for news in news_list:
        news.rating = news.avg_score
        news.save()
    print('ratings updated')
    return 'Success'
