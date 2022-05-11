from django.forms.models import ModelForm
from .models import Subject, Question, Answer, Session, Student


class SubjectForm(ModelForm):
	class Meta:
		model = Subject
		fields = '__all__'
		exclude = ['teacher', ]


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = '__all__'
		exclude = ['teacher', 'subject']


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = '__all__'
		exclude = []

class GeneralSessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['name', 'description','start_datetime','expiration_datetime']

class SessionForm(ModelForm):
	class Meta:
		model = Session
		fields = '__all__'
		exclude = ['teacher', 'subject']


class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['teacher', ]
