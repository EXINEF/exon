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

class SessionAdmin(admin.ModelAdmin):
    model = Session

class ExamAdmin(admin.ModelAdmin):
    model = Exam 

class ExamQuestionAdmin(admin.ModelAdmin):
    model = ExamQuestion

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Session, SessionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamQuestion, ExamQuestionAdmin)