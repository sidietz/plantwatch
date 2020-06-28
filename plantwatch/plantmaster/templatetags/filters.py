from django import template

register = template.Library()

@register.filter
def myround(value, num):
    if type(value) == float:
        if value.is_integer():
            return int(value)
        else:
            f = round(value, num)
            fms = '{:.' + str(num) + 'f}'
            return str(f).replace(".", ",")
    else:
        return value