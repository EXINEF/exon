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
    if not user.groups.filter(name=group_name).exists():
        return False
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name='has_this_answer')
def has_this_answer(exam_question, pk): 
    """
        Checks if an exam_question contains an answer,
        by searching it with its primary key, that's unique for definition.    
    """
    return exam_question.has_this_answer(pk)

@register.filter(name='get_status_of_answer')
def get_status_of_answer(exam_question, pk): 
    """
        Checks if an exam_question contains an answer,
        by searching it with its primary key, that's unique for definition.    
    """
    return exam_question.get_status_of_answer(pk)