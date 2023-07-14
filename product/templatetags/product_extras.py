from django import template


register = template.Library()

@register.filter(name="round")
def round_rate(value):
    return round(value, 1)

