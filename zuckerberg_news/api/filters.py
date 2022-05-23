from django_filters import rest_framework

from news.models import News


class NewsFilter(rest_framework.FilterSet):

    is_favorited = rest_framework.filters.BooleanFilter(method='favorited')

    def favorited(self, queryset, field_name, value):
        if value:
            return queryset.filter(is_in_favorite__user=self.request.user)
        return queryset

    author = rest_framework.filters.CharFilter(
        field_name='author__username',
    )

    class Meta:
        model = News
        fields = ('author', 'is_favorited')
