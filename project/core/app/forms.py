from django.forms.models import ModelForm
from .models import Subject, Question, Answer, Session, Student


class SubjectForm(ModelForm):
	class Meta:
		model = Subject
		fields = '__all__'
		exclude = ['teacher', 'statistics' ]


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = '__all__'
		exclude = ['teacher', 'subject', 'type']


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = '__all__'
		exclude = []


class SessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['name', 'description','start_datetime','expiration_datetime','number_of_questions', 'duration','weight_correct_answer','weight_blank_answer','weight_wrong_answer']


class GeneralSessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['name', 'description','start_datetime','expiration_datetime']

class SettingsSessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['number_of_questions', 'duration','weight_correct_answer','weight_blank_answer','weight_wrong_answer']


class WeightsSessionForm(ModelForm):
	class Meta:
		model = Session
		fields = ['weight_correct_answer','weight_blank_answer','weight_wrong_answer']


class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['session', ]
