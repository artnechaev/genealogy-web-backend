from django.contrib.auth import get_user_model, authenticate
from django.utils import dateformat, dateparse
from djoser.conf import settings
from djoser.serializers import (UserCreateSerializer as BaseUserCreateSerializer,
                                TokenCreateSerializer as BaseTokenCreateSerializer,
                                UserSerializer as BaseUserSerializer)
from rest_framework import serializers

from .models import Note

User = get_user_model()


class UserArticleBooleanField(serializers.BooleanField):
    """
    Поле для преобразования информации о статьях пользователя в булевые переменные.
    manager - менеджер для доступа к списку статей одноименного поля (передаваемого как source) в модели пользователя
    """

    def get_attribute(self, instance):
        user = self.context['request'].user
        manager = getattr(user, self.source)
        return manager.filter(pk=instance.pk).exists()


class UserSerializer(BaseUserSerializer):
    """Переопределенный сериализатор для данных текущего пользователя"""

    class Meta(BaseUserSerializer.Meta):
        fields = (settings.USER_ID_FIELD, 'email', 'first_name', 'last_name', 'photo',
                  'favorite_articles', 'viewed_articles', 'last_article',)


class UserNoteSerializer(serializers.ModelSerializer):
    """Сериализатор для заметок пользователя"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'text', 'date_updated', 'article', 'user')

    def to_representation(self, instance):
        """Изменение формата выводимой даты для отображения на русском с правильными окончаниями"""
        ret = super().to_representation(instance)
        date_updated = dateparse.parse_datetime(ret['date_updated'])
        ret['date_updated'] = dateformat.format(date_updated, 'G:i d E Y')
        return ret


class UserArticleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для информации об избранных и просмотренных статьях пользователя
    """

    favorites = UserArticleBooleanField(required=False, source='favorite_articles')
    viewed = UserArticleBooleanField(required=False, source='viewed_articles')

    class Meta:
        model = User
        fields = ('id', 'favorites', 'viewed')

    def update(self, instance, validated_data):
        """
        Для каждого поля в запросе определяет добавить или удалить текущую статью (instance) в соответствующее
        many-to-many поле модели пользователя (source), получая через него доступ к списку статей
        """
        user = self.context['request'].user

        for field, value in validated_data.items():
            manager = getattr(user, field)
            if value:
                manager.add(instance)
            else:
                manager.remove(instance)
        return instance


class UserCreateSerializer(BaseUserCreateSerializer):
    """Переопределенный сериализатор для регистрации пользователя"""

    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (settings.USER_ID_FIELD, 'email', 'first_name', 'last_name', 'password')

    def validate_email(self, value):
        """
        Нормализация email и проверка на уникальность пользователя,
        т.к. изначальная проверка на уникальность выполняется раньше
        """
        email = User.objects.normalize_email(value)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты уже существует.', code='unique'
            )
        return email


class TokenCreateSerializer(BaseTokenCreateSerializer):
    """Переопределенный сериализатор для получения токена: возврат сообщений об ошибках в конкретном поле"""

    default_error_messages = {
        'email_not_found': settings.CONSTANTS.messages.EMAIL_NOT_FOUND,
        'invalid_password': settings.CONSTANTS.messages.INVALID_PASSWORD_ERROR,
    }

    def validate_email(self, value):
        """Нормализация email"""
        email = User.objects.normalize_email(value)
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if not self.user:
                key_error = 'email_not_found'
                raise serializers.ValidationError(
                    {'email': [self.error_messages[key_error]]}, code=key_error
                )
            elif self.user and not self.user.check_password(password):
                key_error = 'invalid_password'
                raise serializers.ValidationError(
                    {'password': [self.error_messages[key_error]]}, code=key_error
                )
        if self.user and self.user.is_active:
            return attrs
        self.fail('invalid_credentials')
