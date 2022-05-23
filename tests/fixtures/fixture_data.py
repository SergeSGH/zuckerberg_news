import pytest
import time


@pytest.fixture
def news(user):
    from news.models import News
    time.sleep(0.0000001)
    return News.objects.create(
        slug='test_slug_1',
        title='Заголовок тестовой новости 1',
        brief='Краткое содержание новости 1',
        contents='Тестовая новость 1',
        author=user
    )
    

@pytest.fixture
def news_2(user):
    from news.models import News
    time.sleep(0.0000001)
    return News.objects.create(
        slug='test_slug_2',
        title='Заголовок тестовой новости 2',
        brief='Краткое содержание новости 2',
        contents='Тестовая новость 2',
        author=user
    )


@pytest.fixture
def news_3(user):
    from news.models import News
    time.sleep(0.0000001)
    return News.objects.create(
        slug='test_slug_3',
        title='Заголовок тестовой новости 3',
        brief='Краткое содержание новости 3',
        contents='Тестовая новость 3',
        author=user
    )


@pytest.fixture
def news_4(user):
    from news.models import News
    time.sleep(0.0000001)
    return News.objects.create(
        slug='test_slug_4',
        title='Заголовок тестовой новости 4',
        brief='Краткое содержание новости 4',
        contents='Тестовая новость 4',
        author=user
    )

@pytest.fixture
def news_5(user):
    from news.models import News
    time.sleep(0.0000001)
    return News.objects.create(
        slug='test_slug_5',
        title='Заголовок тестовой новости 5',
        brief='Краткое содержание новости 5',
        contents='Тестовая новость 5',
        author=user
    )

@pytest.fixture
def score_1_news(news, user):
    from news.models import Score
    return Score.objects.create(author=user, news=news, score=1)


@pytest.fixture
def score_2_news(news, user_2):
    from news.models import Score
    return Score.objects.create(author=user_2, news=news, score=-1)


@pytest.fixture
def follow_1(user, news):
    from news.models import IsFavorite
    return IsFavorite.objects.create(user=user, news=news)


@pytest.fixture
def follow_2(user_2, news):
    from news.models import IsFavorite
    return IsFavorite.objects.create(user=user_2, news=news)
