from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from filer.fields.image import FilerImageField

User = get_user_model()


class VisibleManager(models.Manager):
    """Менеджер моделей для статей и разделов, возвращающий записи с is_visible == True"""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Section(models.Model):
    """Модель раздела сайта, включающего статьи по одной тематике"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
        verbose_name='Порядок'
    )

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['order']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('section-detail', kwargs={'pk': self.pk})


class Article(models.Model):
    """Модель статьи"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    summary = models.TextField(blank=True, null=True, verbose_name='Краткое содержание')
    text = models.TextField(blank=True, null=True, verbose_name='Текст статьи')
    picture = FilerImageField(
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='article_picture',
        verbose_name='Изображение'
    )
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Раздел'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name='Автор'
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
        verbose_name='Порядок'
    )

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['order']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})
