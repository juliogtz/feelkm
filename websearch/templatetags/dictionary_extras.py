from django import template
from django.template.defaultfilters import stringfilter
import math
import random

register = template.Library()

@register.filter(name='access')
def access(value, arg):
    return value[arg]


@register.filter(name='strip')
@stringfilter
def strip(s):
     return s.strip()


@register.filter(name='replacestr')
@stringfilter
def replacestr(s):
     s = s.replace(' ','-')
     s = s.replace('---','-')
     s = s.replace('--','-')
     s = s.replace('----','-')
     s = s.replace('/','-')
     s = s.replace('(','-')
     s = s.replace(')','-')
     return s


@register.filter(name='replacedigit')
@stringfilter
def replacedigit(n):

    c = len(n)
    if(c==1):
        n='0'+n

    return n

@register.filter(name='intToStr')
@stringfilter
def int_to_string(value):
    return str(value)


@register.filter(name='StrToInt')
@stringfilter
def string_to_int(value):
    return int(value)


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""

def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)


@register.filter(name='shuffle')
def shuffle(arg):
    file = arg[random.randrange(len(arg))]
    return file.file


@register.filter(name='truncatewords_by_chars')
@stringfilter
def truncatewords_by_chars(value, arg):
    """Truncate the text when it exceeds a certain number of characters.
    Delete the last word only if partial.
    Adds '...' at the end of the text.

    Example:

        {{ text|truncatewords_by_chars:25 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value

    if len(value) > length:
        if value[length:length + 1].isspace():
            return value[:length].rstrip() + ''
        else:
            return value[:length].rsplit(' ', 1)[0].rstrip() + ''
    else:
        return value