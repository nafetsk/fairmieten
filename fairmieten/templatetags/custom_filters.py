from django import template
from itertools import groupby
from operator import attrgetter

register = template.Library()

@register.filter
def groupby_typ(diskriminierungen):
    # Group the diskriminierungen by 'typ.name'
    sorted_diskriminierungen = sorted(diskriminierungen, key=attrgetter('typ.name'))
    return {key: list(group) for key, group in groupby(sorted_diskriminierungen, key=attrgetter('typ.name'))}