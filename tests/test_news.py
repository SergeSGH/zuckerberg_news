import pytest

from news.models import News


class TestNewsAPI:

    @pytest.mark.django_db(transaction=True)
    def test_news_not_found(self, client, news):
        response = client.get('/api/news/')

        assert response.status_code != 404, (
            'Страница `/api/news/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_list_not_auth(self, client, news):
        response = client.get('/api/news/')

        assert response.status_code == 200, (
            'Проверьте, что на `/api/news/` при запросе без токена возвращаете статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_single_not_auth(self, client, news):
        response = client.get(f'/api/news/{news.slug}/')

        assert response.status_code == 200, (
            'Проверьте, что на `/api/news/{news.slug}/` при запросе без токена возвращаете статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_get_not_paginated(self, user_client, news, news_2, news_3, news_4, news_5):
        response = user_client.get('/api/news/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/news/` с токеном авторизации возвращается статус 200'
        )

        test_data = response.json()

        # response without pagination must be a list type
        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/api/news/` без пагинации, возвращается список'
        )

        assert len(test_data) == News.objects.count(), (
            'Проверьте, что при GET запросе на `/api/news/` без пагинации возвращается весь список статей'
        )

        news = News.objects.all()[0]
        test_news = test_data[0]
        assert 'slug' in test_news, (
            'Проверьте, что добавили `slug` в список полей `fields` сериализатора модели News'
        )
        assert 'pub_date' in test_news, (
            'Проверьте, что добавили `pub_date` в список полей `fields` сериализатора модели News'
        )
        assert 'author' in test_news, (
            'Проверьте, что добавили `author` в список полей `fields` сериализатора модели News'
        )
        assert 'title' in test_news, (
            'Проверьте, что добавили `title` в список полей `fields` сериализатора модели News'
        )
        assert 'brief' in test_news, (
            'Проверьте, что добавили `brief` в список полей `fields` сериализатора модели News'
        )
        assert 'contents' in test_news, (
            'Проверьте, что добавили `contents` в список полей `fields` сериализатора модели News'
        )
        assert test_news['author'] == news.author.username, (
            'Проверьте, что `author` сериализатора модели News возвращает имя пользователя'
        )

        assert test_news['id'] == news.id, (
            'Проверьте, что при GET запросе на `/api/news/` возвращается весь список новсстй'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_get_paginated(self, user_client, news, news_2, news_3, news_4, news_5):
        base_url = '/api/news/'
        limit = 2
        page = 2
        url = f'{base_url}?limit={limit}&page={page}'
        response = user_client.get(url)
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе `{url}` с токеном авторизации возвращается статус 200'
        )

        test_data = response.json()

        # response with pagination must be a dict type
        assert type(test_data) == dict, (
            f'Проверьте, что при GET запросе на `{url}` с пагинацией, возвращается словарь'
        )
        assert "results" in test_data.keys(), (
            f'Убедитесь, что при GET запросе на `{url}` с пагинацией, ключ `results` присутствует в ответе'
        )
        assert len(test_data.get('results')) == limit, (
            f'Проверьте, что при GET запросе на `{url}` с пагинацией, возвращается корректное количество статей'
        )
        assert test_data.get('results')[0].get('title') == news_3.title, (
            f'Убедитесь, что при GET запросе на `{url}` с пагинацией, '
            'в ответе содержатся корректные статьи'
        )

        news = News.objects.get(title=news_3.title)
        test_news = test_data.get('results')[0]
        assert 'id' in test_news, (
            'Проверьте, что добавили `id` в список полей `fields` сериализатора модели News'
        )
        assert 'title' in test_news, (
            'Проверьте, что добавили `text` в список полей `fields` сериализатора модели News'
        )
        assert 'author' in test_news, (
            'Проверьте, что добавили `author` в список полей `fields` сериализатора модели News'
        )
        assert 'pub_date' in test_news, (
            'Проверьте, что добавили `pub_date` в список полей `fields` сериализатора модели News'
        )
        assert test_news['author'] == news.author.username, (
            'Проверьте, что `author` сериализатора модели News возвращает имя пользователя'
        )

        assert test_news['id'] == news.id, (
            f'Проверьте, что при GET запросе на `{url}` возвращается корректный список статей'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_create(self, user_client, user, news, news_2, news_3, news_4, news_5):
        news_count = News.objects.count()

        data = {}
        response = user_client.post('/api/news/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/news/` с не правильными данными возвращается статус 400'
        )

        data = {'slug':'test_slug_10',
            'title':'Заголовок тестовой новости 10',
            'brief':'Краткое содержание новости 10',
            'contents':'Тестовая новость 10'
        }
        response = user_client.post('/api/news/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/news/` с правильными данными возвращается статус 201'
        )
        assert (
                response.json().get('author') is not None
                and response.json().get('author') == user.username
        ), (
            'Проверьте, что при POST запросе на `/api/news/` автором указывается пользователь,'
            'от имени которого сделан запрос'
        )

        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на `/api/news/` возвращается словарь с данными новой статьи'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('title') == data['title'], msg_error

        assert test_data.get('author') == user.username, (
            'Проверьте, что при POST запросе на `/api/news/` создается статья от авторизованного пользователя'
        )
        assert news_count + 1 == News.objects.count(), (
            'Проверьте, что при POST запросе на `/api/news/` создается статья'
        )
