from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Prefetch
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from .models import Article, Section
from .serializers import ArticleSerializer, ArticleListSerializer, SectionSerializer, ArticleSearchSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для списка статей и отдельной статьи"""

    queryset = Article.visible.select_related('author', 'picture')

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для списка разделов и отдельного раздела"""

    articles = Article.visible.select_related('author', 'picture')

    # Объект Prefetch позволяет передать в prefetch_related только статьи с is_visible == True
    queryset = Section.visible.prefetch_related(Prefetch('articles', queryset=articles))
    serializer_class = SectionSerializer


class ArticleSearchView(mixins.ListModelMixin, GenericViewSet):
    """Представление для списка найденных статей по GET-запросу c параметром query"""

    serializer_class = ArticleSearchSerializer

    def get_queryset(self):
        search_vector = SearchVector('text')
        search_query = SearchQuery(self.request.GET.get('query'))
        search_headline = SearchHeadline(
            'text',
            search_query,
            min_words=17,  # минимальное количество слов в выводимом результате запроса
            start_sel='<span>',
            stop_sel='</span>',
        )
        max_search_results = 30  # максимальное количество выводимых результатов запроса
        queryset = (Article.visible.annotate(headline=search_headline)
                    .annotate(rank=SearchRank(search_vector, search_query))
                    .filter(rank__gte=0.01).order_by('-rank'))
        return queryset.select_related('section')[:max_search_results]
