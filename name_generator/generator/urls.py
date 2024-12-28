from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import MapViewSet, PhraseViewSet

router = DefaultRouter()

router.register('', PhraseViewSet, basename='phrases')

urlpatterns = [
    path('phrases/', include(router.urls)),
    path('', MapViewSet.as_view(), name='map'),
]
