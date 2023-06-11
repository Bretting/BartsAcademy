
from django import template
import random

register = template.Library()


@register.filter
def shuffle(arg):
    # slice it, cast it to list
    my_list = list(arg[:])
    random.shuffle(my_list)
    return my_list