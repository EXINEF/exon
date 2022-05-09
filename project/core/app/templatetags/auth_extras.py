from django import template
from django.contrib.auth.models import Group 

"""
    Allows to register a custom Django Html Tag,
"""

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    """
        Returns all groups the user belongs to,
        if belongs to No Groups return FALSE
    """
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False