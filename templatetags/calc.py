from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg) * 100 if float(arg) != 0 else ''
    except (ValueError, TypeError):
        return ''


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''