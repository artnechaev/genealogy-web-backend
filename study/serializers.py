from rest_framework import serializers

from .models import Article, Section


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для отдельной статьи"""

    # Вывод даты в нужном формате, имени и фамилии автора вместо id
    date_added = serializers.DateTimeField(format='%d/%m/%Y')
    date_updated = serializers.DateTimeField(format='%d/%m/%Y')
    author = serializers.CharField(source='author.get_full_name')
    picture = serializers.ImageField()

    class Meta:
        model = Article
        fields = ('id', 'slug', 'name', 'picture', 'text', 'date_added', 'date_updated', 'author')


class ArticleListSerializer(ArticleSerializer):
    """Сериализатор для списка статей"""

    class Meta:
        model = Article
        fields = ('id', 'slug', 'name', 'picture', 'summary', 'date_added', 'date_updated', 'author')


class ArticleSearchSerializer(serializers.ModelSerializer):
    """Сериализатор для поиска по тексту статьи"""

    text = serializers.CharField(source='headline')
    section_name = serializers.CharField(source='section.name')

    class Meta:
        model = Article
        fields = ('id', 'slug', 'name', 'text', 'section_id', 'section_name')


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для разделов"""

    articles = ArticleListSerializer(many=True)

    class Meta:
        model = Section
        fields = ('id', 'slug', 'name', 'articles')
