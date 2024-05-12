from django import template

register = template.Library()


@register.filter
def split_str(value, separator):
    return value.split(separator)
