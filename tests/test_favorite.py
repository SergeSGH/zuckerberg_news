import pytest


class TestfavorigteAPI:

    @pytest.mark.django_db(transaction=True)
    def test_favorite_not_found(self, client, news, follow_1, follow_2):
        response = client.get(f'/api/news/{news.slug}/favorite/')

        assert response.status_code != 404, (
            'Страница `/api/news/<news.slug>/favorite/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code != 500, (
            'Страница `/api/news/<news.slug>/favorite/` не может быть обработана вашим сервером, проверьте view-функцию в *views.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_not_auth(self, client, news, follow_1, follow_2):
        response = client.get(f'/api/news/{news.slug}/favorite/')
        assert response.status_code == 401, (
            'Проверьте, что `/api/news/<news.slug>/favorite/` при GET запросе без токена возвращает статус 401'
        )

        data = {}
        response = client.post(f'/api/news/{news.slug}/favorite/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что `/api/news/<news.slug>/favorite/` при POST запросе без токена возвращает статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_delete(self, user_client, news, user, follow_1, follow_2):
        response = user_client.delete(f'/api/news/{news.slug}/favorite/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/news/<news.slug>/favorite/` с токеном авторизации возвращается статус 204'
        )


    @pytest.mark.django_db(transaction=True)
    def test_favorite_create(self, user_client, news, follow_2, user, user_2):

        data = {}
        response = user_client.post(f'/api/news/{news.slug}/favorite/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/<news.slug>/favorite/` возвращается статус 201'
        )

        response = user_client.post(f'/api/news/{news.slug}/favorite/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/<news.slug>/favorite/` '
            'при подписке на новость повторно возвращается статус 400'
        )
