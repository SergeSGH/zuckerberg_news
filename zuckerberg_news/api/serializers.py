from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from news.models import News, IsFavorite, Score


from django.contrib.auth import get_user_model


User = get_user_model()


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
            'slug', 'title', 'author',
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


class IsFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        #read_only=True,
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    news = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=News.objects.all()
    )

    class Meta:
        fields = ('user', 'news')
        model = IsFavorite

        validators = [
            UniqueTogetherValidator(
                queryset=IsFavorite.objects.all(),
                fields=['user', 'news']
            )
        ]


class ScoreSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        #read_only=True,
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    #news = serializers.PrimaryKeyRelatedField(
    #    #read_only=True,
    #    queryset=News.objects.all()
    #)

    class Meta:
        fields = ('author', 'score')
        model = Score

