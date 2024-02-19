from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.decorators import action


class UserNoteViewSetSchema(OpenApiViewExtension):
    target_class = 'users.views.UserNoteViewSet'

    def view_replacement(self):
        @extend_schema(tags=['User notes'])
        @extend_schema_view(
            create=extend_schema(
                summary='Создание заметки по статье',
                description='Endpoint для создания заметки по статье',
            ),
            list=extend_schema(
                summary='Получение списка всех заметок пользователя',
                description='Endpoint для списка всех заметок пользователя',
                parameters=[
                    OpenApiParameter(
                        name='article',
                        location=OpenApiParameter.QUERY,
                        description='id статьи для возврата заметок по ней',
                        required=False,
                        type=OpenApiTypes.INT
                    ),
                ],
            ),
            retrieve=extend_schema(
                summary='Получение информации об отдельной заметке',
                description='Endpoint для отдельной заметки',
            ),
            update=extend_schema(
                summary='Изменение существующей заметки',
                description='Endpoint для изменения существующей заметки',
            ),
            partial_update=extend_schema(
                summary='Частичное изменение существующей заметки',
                description='Endpoint для частичного изменения существующей заметки',
            ),
            destroy=extend_schema(
                summary='Удаление существующей заметки',
                description='Endpoint для удаления существующей заметки',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class UserArticleViewSetSchema(OpenApiViewExtension):
    target_class = 'users.views.UserArticleViewSet'

    def view_replacement(self):
        @extend_schema(tags=['User articles'])
        @extend_schema_view(
            list=extend_schema(
                summary='Получение списка статей с информацией о нахождении в просмотренных/избранных',
                description='Endpoint для списка статей с информацией о нахождении в списках просмотренных/избранных',
            ),
            retrieve=extend_schema(
                summary='Получение информации о нахождении отдельной статьи в просмотренных/избранных',
                description='Endpoint для информации о нахождении отдельной статьи в списках просмотренных/избранных',
            ),
            update=extend_schema(
                summary='Добавление/удаление статьи из списка просмотренных/избранных',
                description='Endpoint для добавления/удаления статьи из списка просмотренных/избранных',
            ),
            partial_update=extend_schema(
                summary='Добавление/удаление статьи из списка просмотренных/избранных',
                description='Endpoint для добавления/удаления статьи из списка просмотренных/избранных',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class TokenCreateViewSchema(OpenApiViewExtension):
    target_class = 'djoser.views.TokenCreateView'

    def view_replacement(self):
        @extend_schema(tags=['Token-based authentication'])
        @extend_schema_view(
            post=extend_schema(
                summary='Получение токена аутентификации пользователя',
                description='Endpoint для получения токена аутентификации пользователя',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class TokenDestroyViewSchema(OpenApiViewExtension):
    target_class = 'djoser.views.TokenDestroyView'

    def view_replacement(self):
        @extend_schema(tags=['Token-based authentication'])
        @extend_schema_view(
            post=extend_schema(
                summary='Выход пользователя из системы и удаление токена',
                description='Endpoint для выхода пользователя из системы и удаления токена',
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class UserViewSetSchema(OpenApiViewExtension):
    target_class = 'djoser.views.UserViewSet'

    def view_replacement(self):
        @extend_schema(tags=['User registration & update'])
        @extend_schema_view(
            create=extend_schema(
                summary='Регистрация нового пользователя',
                description='Endpoint для регистрации нового пользователя',
            ),
            list=extend_schema(exclude=True),
            retrieve=extend_schema(exclude=True),
            update=extend_schema(exclude=True),
            partial_update=extend_schema(exclude=True),
            destroy=extend_schema(exclude=True),
            activation=extend_schema(exclude=True),
            resend_activation=extend_schema(exclude=True),
            set_password=extend_schema(exclude=True),
            reset_password=extend_schema(exclude=True),
            reset_password_confirm=extend_schema(exclude=True),
            set_username=extend_schema(exclude=True),
            reset_username=extend_schema(exclude=True),
            reset_username_confirm=extend_schema(exclude=True),
        )
        class Fixed(self.target_class):
            @extend_schema(
                summary="Получение детальной информации о пользователя",
                description="Endpoint для получения детальной информации о пользователе",
                methods=['get'])
            @extend_schema(
                summary="Изменение информации о пользователе",
                description="Endpoint для изменения информации о пользователе",
                methods=['put'])
            @extend_schema(
                summary="Частичное изменение информации о пользователе",
                description="Endpoint для частичного изменения информации о пользователе",
                methods=['patch'])
            @extend_schema(
                summary="Удаление профиля пользователя",
                description="Endpoint для удаления профиля пользователя",
                methods=['delete'])
            @action(['get', 'put', 'patch', 'delete'], detail=False)
            def me(self, request, *args, **kwargs):
                pass
            pass

        return Fixed
