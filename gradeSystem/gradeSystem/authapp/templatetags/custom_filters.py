from django import template

register = template.Library()

@register.filter
def join_class_names(queryset, separator=", "):
    return separator.join([obj.class_name for obj in queryset])

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)