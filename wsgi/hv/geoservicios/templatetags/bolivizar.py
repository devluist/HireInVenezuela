from django import template
from geoservicios.views import PRECIO_POR_DOLAR as ppd

register = template.Library()


@register.filter("bf")
def bf(valor):
	return valor * ppd
