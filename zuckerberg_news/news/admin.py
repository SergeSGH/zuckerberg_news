from django.contrib import admin

from .models import IsFavorite, News, Score, User


class UserAdmin(admin.ModelAdmin):

    def news_count(self, obj):
        return obj.news.all().count()

    news_count.short_description = 'Количество публикаций'

    list_display = (
        'id',
        'username',
        'email',
        'news_count'
    )
    ordering = ('id',)
    empty_value_display = '--empty--'


class ScoreInline(admin.StackedInline):
    model = Score
    extra = 0


class IsFavoriteInline(admin.StackedInline):
    model = IsFavorite
    extra = 0


class NewsAdmin(admin.ModelAdmin):

    def favorite_count(self, obj):
        return obj.favorited.all().count()

    favorite_count.short_description = 'Добавлено в избранное'

    inlines = (ScoreInline, IsFavoriteInline)
    list_display = (
        'id',
        'slug',
        'title',
        'author',
        'brief',
        'contents',
        'views',
        'rating'
    )
    search_fields = (
        'slug',
        'title',
        'author__username',
        'author__email'
    )
    list_filter = ('author__username',)
    empty_value_display = '--empty--'


admin.site.register(User, UserAdmin)
admin.site.register(News, NewsAdmin)
