from django.template.defaultfilters import slugify as django_slugify
from datetime import datetime as dt

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(value):
    """Расширение slugify() для обработки кириллицы"""
    value = str(value).lower()
    return django_slugify(''.join(alphabet.get(char, char) for char in value))


def get_image_path(instance, filename):
    """Создание пути для загружаемой картинки с текущей датой и обработка кириллицы в имени"""
    now = dt.now()
    model = instance._meta.model_name
    name, ext = filename.rsplit('.', 1)

    return f'{model}s/{now.strftime("%Y/%m/%d")}/{slugify(name)}.{ext}'
