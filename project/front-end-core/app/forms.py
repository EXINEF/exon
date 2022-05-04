from django.forms.models import ModelForm
from .models import Subject, Question, Answer

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['teacher',]

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['teacher','subject']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        exclude = []
