from django import template

register = template.Library()
# Simple filter for universal display of the numbers (PL numbers have "," so it needs to be converted to ".")
@register.filter
def dot_notation(value):
    """replace comma decimal separator with a dot."""
    
    if value is None:
        return ""
    
    return str(value).replace(',','.')
    