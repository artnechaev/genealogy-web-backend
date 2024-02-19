from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm
from .models import User, Note


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'photo',
                                         'favorite_articles', 'viewed_articles', 'last_article')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-is_staff', 'email')
    filter_horizontal = ('groups', 'user_permissions', 'favorite_articles', 'viewed_articles')
    save_on_top = True


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_full_name', 'summary', 'article', 'date_updated')
    list_display_links = ('user', 'user_full_name')
    list_filter = ('user', 'date_updated')
    search_fields = ('user', 'text')

    @admin.display(description='Текст')
    def summary(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text

    @admin.display(description='Имя пользователя')
    def user_full_name(self, obj):
        return obj.user.get_full_name()


admin.site.site_title = 'Генеалогия'  # заголовок вкладки
admin.site.site_header = 'Админ-панель проекта "Генеалогия"'  # первый заголовок
# admin.site.index_title = 'Администрирование сайта' # второй заголовок

# admin.site.unregister(Group)
