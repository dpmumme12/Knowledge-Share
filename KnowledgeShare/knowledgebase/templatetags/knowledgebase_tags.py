from django import template
from ..models import Folder, Article

register = template.Library()


@register.filter
def is_folder_instance(obj):
    return isinstance(obj, Folder)


@register.filter
def is_article_instance(obj):
    return isinstance(obj, Article)
