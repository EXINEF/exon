from django.contrib import admin
from .models import *

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    model = Teacher

class SubjectAdmin(admin.ModelAdmin):
    model = Subject

class AnswerAdmin(admin.ModelAdmin):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    model = Question

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)