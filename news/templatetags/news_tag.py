from django.shortcuts import get_object_or_404
from ..views import Tag
from django import template

register = template.Library()


@register.inclusion_tag('component/navBar.html')
def navBar():
    tags = Tag.objects.all()

    return {
        'tags': tags,
    }


