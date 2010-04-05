from django import template

register = template.Library()

@register.filter
def paramify(value):
    return value.replace('+', '%2B')
