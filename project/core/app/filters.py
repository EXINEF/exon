from django.forms import CharField
import django_filters
from django_filters import CharFilter

from .models import *

class QuestionFilter(django_filters.FilterSet):
    text = CharFilter(field_name='text', lookup_expr='icontains')
    
    class Meta:
        model = Question
        exclude = ['teacher', 'subject','creation_datetime']