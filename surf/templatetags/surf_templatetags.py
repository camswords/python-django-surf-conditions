import urllib

from django import template

register = template.Library()


@register.filter
def get_value(dictionary, key_name, default_value=None):
    return dictionary.get(key_name, default_value)


@register.simple_tag
def query_params(other_params, **kwargs):
    merged = {**(other_params or {}), **kwargs}
    return '?' + urllib.parse.urlencode(merged)
