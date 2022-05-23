import pytest

from news.models import Score

class TestScoreAPI:

    @pytest.mark.django_db(transaction=True)
    def test_score_not_found(self, user_client, news, score_1_news):
        response = user_client.get(f'/api/news/{news.slug}/score/')

        assert response.status_code != 404, (
            'Страница `/api/news/{news.slug}/score/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_score_get(self, user_client, news, score_1_news):
        response = user_client.get(f'/api/news/{news.slug}/score/')

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/news/{news.slug}/score/` '
            'с токеном авторизации возвращаетсся статус 200'
        )
        test_data = response.json()
        assert type(test_data) == dict, (
            'Проверьте, что при GET запросе на `/api/news/{news.slug}/score/` возвращается словарь'
        )

        score = Score.objects.filter(news=news).first()
        test_score = test_data
        assert 'score' in test_data, (
            'Проверьте, что добавили `score` в список полей `fields` сериализатора модели Score'
        )
        assert test_score['score'] == score.score, (
            'Проверьте, что `score` сериализатора модели Score возвращает корректную оценку'
        )

    @pytest.mark.django_db(transaction=True)
    def test_score_patch(self, user_client, news, score_1_news):
        data = {'score': 1}
        response = user_client.patch(f'/api/news/{news.slug}/score/', data=data)

        assert response.status_code == 201, (
            'Проверьте что при изменении оценки запросом методом PATCH '
            'по адресу  `/api/news/{news.slug}/score/` возвращается статус 201'
        )

    @pytest.mark.django_db(transaction=True)
    def test_score_patch_not_correct(self, user_client, news, score_1_news):
        data = {'score': 2}
        response = user_client.patch(f'/api/news/{news.slug}/score/', data=data)

        assert response.status_code == 400, (
            'Проверьте что при изменении оценки запросом методом PATCH на некорректную'
            'по адресу  `/api/news/{news.slug}/score/` возвращается статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_score_delete(self, user_client, news, score_1_news):
        response = user_client.delete(f'/api/news/{news.slug}/score/')

        assert response.status_code == 204, (
            'Проверьте что при удалении оценки запросом методом DELETE'
            'по адресу  `/api/news/{news.slug}/score/` возвращается статус 204'
        )