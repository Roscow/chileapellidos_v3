# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='formato_miles')
def formato_miles(numero):
    return '{0:,}'.format(numero).replace(',', '.')
