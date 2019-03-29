from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def moeda(valor):
    if valor != None:
        import locale
        locale.setlocale( locale.LC_ALL, '' )
        return locale.currency( valor, grouping=True )
    return ''
