from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from news.models import IsFavorite, News, Score, User
from .pagination import NewsPagination
from .permissions import IsAuthor, ReadOnly
from .serializers import NewsSerializer, NewsSerializerShort, ScoreSerializer

User = get_user_model()


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReadOnly | IsAuthor,
    )
    queryset = News.objects.all()
    pagination_class = NewsPagination
    lookup_field = 'slug'

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, **kwargs):
        news = get_object_or_404(News, slug=self.kwargs.get('slug'))
        if request.method == 'POST':
            if IsFavorite.objects.filter(
                news=news, user=self.request.user
            ).exists():
                return Response(
                    'Новость уже в избранном',
                    status=status.HTTP_400_BAD_REQUEST
                )
            IsFavorite.objects.create(
                news=news, user=self.request.user
            )
            return Response(
                'Новость добавлена в избранное',
                status=status.HTTP_201_CREATED
            )
        if not IsFavorite.objects.filter(
            news=news, user=self.request.user
        ).exists():
            return Response(
                'Новости нет в избранном',
                status=status.HTTP_400_BAD_REQUEST
            )
        record = IsFavorite.objects.filter(
            news=news, user=self.request.user
        )
        record.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=('get', 'post', 'patch', 'delete'),
        url_path='score',
        permission_classes=(IsAuthenticated,),
    )
    def score(self, request, **kwargs):
        news = get_object_or_404(News, slug=self.kwargs.get('slug'))
        if request.method == 'GET':
            if Score.objects.filter(
                news=news, author=self.request.user
            ).exists():
                score = Score.objects.get(news=news, author=self.request.user)
                serializer = ScoreSerializer(score)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                    'Оценки нет',
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'POST':
            if Score.objects.filter(
                news=news, author=self.request.user
            ).exists():
                return Response(
                    'Оценка уже поставлена',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ScoreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    author=self.request.user,
                    news=news
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                'kk',
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'PATCH':
            if not Score.objects.filter(
                news=news, author=self.request.user
            ).exists():
                return Response(
                    'Оценки нет',
                    status=status.HTTP_400_BAD_REQUEST
                )
            score = Score.objects.get(
                news=news, author=self.request.user
            )
            serializer = ScoreSerializer(score, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save(
                    author=self.request.user,
                    news=news
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if not Score.objects.filter(
                news=news, author=self.request.user
            ).exists():
                return Response(
                    'Оценки нет',
                    status=status.HTTP_400_BAD_REQUEST
                )
            score=Score.objects.get(
                news=news, author=self.request.user
            )
            score.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )


class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReadOnly | IsAuthor,
    )

    def get_queryset(self):
        news_slug = self.kwargs.get('news_slug')
        news = get_object_or_404(News, slug=news_slug)
        queryset = news.scores.all()
        return queryset

    def perform_create(self, serializer):
        news_slug = self.kwargs.get('news_slug')
        news = get_object_or_404(News, slug=news_slug)
        print(news.brief)
        if not Score.objects.filter(
            author=self.request.user, news=news
        ).exists():
            serializer.save(
                author=self.request.user,
                news=news
            )

    def perform_update(self, obj, serializer):
        news_slug = self.kwargs.get('news_slug')
        news = get_object_or_404(News, slug=news_slug)
        serializer = serializer(
            obj, data=self.request.data, partial=True
        )
        serializer.save()

