from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from news.models import User, News, IsFavorite, Score
from .permissions import IsAuthor, ReadOnly
from .pagination import NewsPagination
from .serializers import (NewsSerializer,
                          IsFavoriteSerializer, ScoreSerializer)


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

    #def perform_create(self, serializer):
    #    serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, **kwargs):
        news = get_object_or_404(News, slug=self.kwargs.get('slug'))
        serializer = NewsSerializer(news)
        return self.sub_create_del(request, IsFavorite, serializer, news)

    def sub_create_del(self, request, model, serializer, news):
        if request.method == 'POST':
            if model.objects.filter(
                news=news, author=self.request.user
            ).exists():
                return Response(
                    'Новость уже в избранном',
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.create(
                news=news, author=self.request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if not model.objects.filter(
            news=news, author=self.request.user
        ).exists():
            return Response(
                'Новости',
                status=status.HTTP_400_BAD_REQUEST
            )
        record = model.objects.filter(
            news=news, author=self.request.user
        )
        record.delete()
        return Response(
            'Новость удалена из избранного',
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

        #return Response(
        #    'Новости',
        #    status=status.HTTP_400_BAD_REQUEST
        #)

    def perform_update(self, serializer):
        news_slug = self.kwargs.get('news_slug')
        news = get_object_or_404(News, slug=news_slug)
        serializer.save(
            author=self.request.user
            #post=post
        )