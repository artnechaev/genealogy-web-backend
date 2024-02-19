from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from study.models import Article
from .models import Note
from .serializers import UserNoteSerializer, UserArticleSerializer


class UserNoteViewSet(viewsets.ModelViewSet):
    """Представление для заметок пользователя"""

    serializer_class = UserNoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Получение всех заметок текущего пользователя и заметок по определенной статье"""
        user = self.request.user
        queryset = Note.objects.filter(user=user)
        article_id = self.request.GET.get('article')
        if article_id:
            queryset = queryset.filter(article=article_id)
        return queryset


class UserArticleViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """Представление для информации об избранных и просмотренных статьях пользователя"""

    queryset = Article.visible.all()
    serializer_class = UserArticleSerializer
    permission_classes = (IsAuthenticated,)
