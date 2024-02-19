from adminsortable2.admin import SortableAdminMixin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.options import ThumbnailOptions

from .models import Section, Article


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget(), label='Текст статьи', required=False)

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Section)
class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('num', 'name', 'slug', 'is_visible', 'order')
    list_display_links = ('num', 'name')
    list_editable = ('is_visible',)
    list_filter = ('is_visible',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15

    @admin.display(description='№')
    def num(self, obj):
        """Отображение поля order в качестве № раздела"""
        return obj.order


@admin.register(Article)
class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('num', 'name', 'section', 'is_visible', 'article_picture', 'order')
    list_display_links = ('num', 'name')
    list_editable = ('is_visible',)
    list_filter = ('section', 'is_visible', 'date_updated')
    search_fields = ('name', 'summary', 'text')
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 15
    form = ArticleAdminForm
    save_on_top = True

    @admin.display(description='№')
    def num(self, obj):
        """Отображение поля order в качестве № статьи"""
        return obj.order

    @admin.display(description='Изображение')
    def article_picture(self, obj):
        """Отображение миниатюры изображения статьи в списке"""
        try:
            thumbnail_options = ThumbnailOptions({'size': (40, 40), 'crop': True})
            thumbnail = get_thumbnailer(obj.picture).get_thumbnail(thumbnail_options)
            return mark_safe(f'<img src="{thumbnail.url}">')
        except (AttributeError, ValueError):
            return ''
