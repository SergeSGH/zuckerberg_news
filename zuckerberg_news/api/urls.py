from django.urls import include, path
from rest_framework import routers

from .views import NewsViewSet, ScoreViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router_v1.urls)),
    #path(r'^news/(?P<news_slug>\w+)/score/', ScoreViewSet.as_view(
    #    {'get': 'list',
    #    'post': 'create',
    #    'patch': 'update',
    #    'delete': 'destroy'})
    #),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
