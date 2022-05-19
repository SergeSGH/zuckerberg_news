from django.urls import include, path
from rest_framework import routers

from .views import NewsViewSet, ScoreViewSet

router_v1 = routers.DefaultRouter()
#router_v1.register('users', UserViewSet, basename='users')
router_v1.register('news', NewsViewSet, basename='news')
router_v1.register(r'^news/(?P<news_slug>\w+)/score',
                   ScoreViewSet, basename=r'^score')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
