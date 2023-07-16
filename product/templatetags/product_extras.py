from django import template


register = template.Library()


@register.filter(name="round")
def round_rate(value):
    if value is not None:
        return round(value, 1)
