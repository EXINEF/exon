from django.forms.models import ModelForm
from .models import Subject

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['teacher',]
