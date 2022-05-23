from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import NewsFilter

from django.db.models import Avg
from news.models import IsFavorite, News, Score, User
from .pagination import NewsPagination
from .permissions import IsAuthor, ReadOnly
from .serializers import NewsSerializer, ScoreSerializer

User = get_user_model()


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReadOnly | IsAuthor,
    )
    queryset = News.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = NewsFilter
    ordering_fields = ('pub_date', 'views', 'rating')
    pagination_class = NewsPagination
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        news = self.get_object()
        if not news.views:
            news.views = 1
        else:
            news.views += 1
        news.save()
        return super().retrieve(self, request, *args, **kwargs)

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
                news.rating = news.scores.aggregate(Avg('score'))['score__avg']
                news.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
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
            serializer = ScoreSerializer(
                score, data=self.request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save(
                    author=self.request.user,
                    news=news
                )
                news.rating = news.scores.aggregate(Avg('score'))['score__avg']
                news.save()
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
            score = Score.objects.get(
                news=news, author=self.request.user
            )
            score.delete()
            news.rating = news.scores.aggregate(Avg('score'))['score__avg']
            news.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
