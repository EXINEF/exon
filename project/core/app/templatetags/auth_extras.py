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

@register.filter(name='has_this_answer')
def has_this_answer(main_question, pk): 
    """
        Returns all groups the user belongs to,
        if belongs to No Groups return FALSE
    """
    return main_question.has_this_answer(pk)