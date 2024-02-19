from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Менеджер моделей для модели пользователя User с полями email and password (без поля username)"""

    def _create_user(self, username, email, password, **extra_fields):
        """Создание и сохранение пользователя с переданными полями email и password"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return super().create_user(username=None, email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return super().create_superuser(username=None, email=email, password=password, **extra_fields)


class User(AbstractUser):
    """Расширенная модель пользователя"""

    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        help_text=_(
            'Обязательное поле. Не более 254 символов.'
        ),
        error_messages={
            'unique': 'Пользователь с таким адресом электронной почты уже существует.'
        },
    )
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')
    favorite_articles = models.ManyToManyField(
        'study.Article',
        blank=True,
        related_name='favorites',
        verbose_name='Избранное')
    viewed_articles = models.ManyToManyField(
        'study.Article',
        blank=True,
        related_name='viewed',
        verbose_name='Просмотренное')
    last_article = models.ForeignKey(
        'study.Article',
        blank=True, null=True,
        related_name='last',
        on_delete=models.SET_NULL,
        verbose_name='Последняя статья')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Note(models.Model):
    """Модель для хранения заметок пользователя"""

    text = models.TextField(verbose_name='Текст заметки')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Пользователь')
    article = models.ForeignKey(
        'study.Article',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Статья'
    )

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-date_updated']

    def __str__(self):
        return f'Заметка {self.id} ({self.user.get_full_name()})'
