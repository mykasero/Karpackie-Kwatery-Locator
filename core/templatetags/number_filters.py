from django import template

register = template.Library()

@register.filter
def dot_notation(value):
    """replace comma decimal separator with a dot."""
    
    if value is None:
        return ""
    
    return str(value).replace(',','.')
    