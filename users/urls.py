from django.urls import path, include
from rest_framework import routers

from .views import UserNoteViewSet, UserArticleViewSet

# app_name = 'users'

router = routers.DefaultRouter()
router.register('notes', UserNoteViewSet, basename='user-note')
router.register('articles', UserArticleViewSet, basename='user-article')

urlpatterns = [
    path('', include(router.urls))
]
