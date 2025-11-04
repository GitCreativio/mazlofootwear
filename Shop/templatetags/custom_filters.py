from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter(name='get')
def get(value, arg):
    return value.get(arg, None)

@register.filter(name='items')
def items(value):
    return value.items()

@register.filter(name='json')
def json(value):
    return value