from django import template
from itertools import groupby
from operator import attrgetter
from urllib.parse import urlencode

register = template.Library()

@register.filter
def groupby_typ(diskriminierungen):
    # Group the diskriminierungen by 'typ.name'
    sorted_diskriminierungen = sorted(diskriminierungen, key=attrgetter("typ.name"))
    grouped = {
        key: list(group)
        for key, group in groupby(sorted_diskriminierungen, key=attrgetter("typ.name"))
    }
    # Rassismus an erster Stelle
    if "Rassismus" in grouped:
        # rassismus aus dem Dict entfernen
        rassismus_group = {"Rassismus": grouped.pop("Rassismus")}
        # neues Erstellen mit Rassismus am Anfang und dem Rest dahinter
        grouped = {**rassismus_group, **grouped}
    return grouped

    
@register.filter
def params_minus(query_params, param_to_remove):
    params = query_params.copy()
    if param_to_remove in params:
        del params[param_to_remove]
    new_query_string = urlencode(params)
    return new_query_string

@register.simple_tag
def params_plus(query_params, param_to_add, value):
    params = query_params.copy()
    params[param_to_add] = value
    new_query_string = urlencode(params)
    return new_query_string

@register.filter
def get_item(dictionary, key):
    """Retrieve an item from a dictionary by key."""
    return dictionary.get(key, None)

@register.filter
def attribute(obj, attr):
    """Retrieve an attribute from an object or handle related items."""
    # First, try to get the attribute from the object
    attribute_value = getattr(obj, attr, None)

    # If the attribute is a many-to-many relation, return all related items
    if attribute_value and hasattr(attribute_value, 'all'):
        return attribute_value.all()
    
    # Otherwise, return the attribute value
    return attribute_value