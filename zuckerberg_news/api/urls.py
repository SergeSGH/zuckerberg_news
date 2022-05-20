from django.urls import include, path
from rest_framework import routers

from .views import NewsViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
