from django import template

register = template.Library()


@register.filter
def get_value(dictionary, key_name, default_value=None):
    return dictionary.get(key_name, default_value)
