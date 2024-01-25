from django import template

from transliterate import slugify

register = template.Library()


@register.filter()
def get_slug(text):
    return slugify(text, language_code="ru")
