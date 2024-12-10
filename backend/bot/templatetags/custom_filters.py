from django import template

register = template.Library()
@register.filter
def skip_every_even(values):
    return [value for index, value in enumerate(values) if index % 2 == 0]

@register.filter
def skip_every_odd(values):
    return [value for index, value in enumerate(values) if index % 2 != 0]
