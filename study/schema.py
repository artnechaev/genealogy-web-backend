from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, OpenApiExample


class ArticleViewSetSchema(OpenApiViewExtension):
    target_class = 'study.views.ArticleViewSet'

    def view_replacement(self):
        @extend_schema(tags=['Articles & Sections'])
        @extend_schema_view(
            list=extend_schema(
                summary='Получение списка cтатей',
                description='Endpoint для списка статей с кратким описанием',
            ),
            retrieve=extend_schema(
                summary='Получение детальной информации о статье',
                description='Endpoint для отдельной статьи с полным описанием',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class SectionViewSetSchema(OpenApiViewExtension):
    target_class = 'study.views.SectionViewSet'

    def view_replacement(self):
        @extend_schema(tags=['Articles & Sections'])
        @extend_schema_view(
            list=extend_schema(
                summary='Получение списка разделов',
                description='Endpoint для списка разделов со статьями',
            ),
            retrieve=extend_schema(
                summary='Получение информации об отдельном разделе',
                description='Endpoint для отдельного раздела со статьями',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class ArticleSearchViewSchema(OpenApiViewExtension):
    target_class = 'study.views.ArticleSearchView'

    def view_replacement(self):
        @extend_schema(tags=['Search'])
        @extend_schema_view(
            list=extend_schema(
                summary='Поиск информации в текстах статей',
                description='Endpoint для поиска информации в текстах статей',
                parameters=[
                    OpenApiParameter(
                        name='query',
                        location=OpenApiParameter.QUERY,
                        description='Запрос для поиска',
                        required=True,
                        type=OpenApiTypes.STR
                    ),
                ],
            )
        )
        class Fixed(self.target_class):
            pass

        return Fixed
