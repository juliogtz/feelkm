from django import template
from django.template.defaultfilters import stringfilter
import math

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
        n="0"+n

    return n

@register.filter(name='intToStr')
@stringfilter
def int_to_string(value):
    return str(value)