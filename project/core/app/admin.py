from django.contrib import admin
from .models import *


# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
	model = Teacher
	
	list_display = ('__str__', 'user', 'full_name')
	search_fields = ['full_name']


class SubjectAdmin(admin.ModelAdmin):
	model = Subject
	
	list_display = ('__str__', 'name', 'teacher')
	search_fields = ['name']


class AnswerAdmin(admin.ModelAdmin):
	model = Answer


class QuestionAdmin(admin.ModelAdmin):
	model = Question


class SessionAdmin(admin.ModelAdmin):
	model = Session


class ExamAdmin(admin.ModelAdmin):
	model = Exam


class ExamQuestionAdmin(admin.ModelAdmin):
	model = ExamQuestion


class StudentAdmin(admin.ModelAdmin):
	model = Student

class AccessAdmin(admin.ModelAdmin):
	model = Access

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Session, SessionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamQuestion, ExamQuestionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Access, AccessAdmin)