from django.urls import path, include
from rest_framework import routers

from .views import ArticleViewSet, SectionViewSet, ArticleSearchView

# app_name = 'study'

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'search', ArticleSearchView, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
