from django import template

register = template.Library()

@register.filter
def replace_nan(value):
    return '' if value == 'nan' else value
