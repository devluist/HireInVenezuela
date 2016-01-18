from django import template
import decimal

register = template.Library()


@register.filter("es_entero")
def es_entero(valor):
	return True if valor == valor.to_integral_value() else False
