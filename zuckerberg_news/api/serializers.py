from django.contrib.auth import get_user_model
from rest_framework import serializers

from news.models import IsFavorite, News, Score

User = get_user_model()



class NewsSerializerShort(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id', 'slug', 'title', 'author',
            'brief', 'contents', 'views',
            'rating'
        )
        read_only_fields = ('views', 'rating')
        model = News


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    score = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'slug', 'title', 'author',
            'brief', 'contents', 'views',
            'rating', 'score', 'is_favorite'
        )
        read_only_fields = ('views', 'rating')
        model = News

    def get_score(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if Score.objects.filter(
                author=user, news=obj
            ).exists():
                return Score.objects.get(
                    author=user, news=obj
                ).score
            return None
        return None

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return IsFavorite.objects.filter(
                user=user, news=obj
            ).exists()
        return False


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('score',)
        model = Score
