from django import template

register = template.Library()


@register.filter
def u(value):
    print(value)
    return str(value).encode()
