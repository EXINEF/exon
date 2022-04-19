from django.urls import path
from .views import *
from .views_teacher import *

urlpatterns = [
    path('', indexPage, name='index'),

    path('student/login', studentLogin, name='student-login'),
    path('student/exam', studentExam, name='student-exam'),
    path('student/result', studentResult, name='student-result'),

    path('teacher/login', teacherLogin, name='teacher-login'),
    path('teacher/dashboard', dashboard, name='teacher-dashboard'),
    path('logout', logoutPage, name='logout'),
    
    # SUBJECT
    path('teacher/subject/<str:pk>', subject, name='teacher-subject'),
    path('teacher/add-subject', addSubject, name='teacher-add-subject'),
    path('teacher/delete-subject/<str:pk>', deleteSubject, name='teacher-delete-subject'),
    path('teacher/all-questions/<str:pk>', allQuestions, name='teacher-all-questions'),

    # QUESTION
    path('teacher/question/<str:pk>', question, name='teacher-question'),
    path('teacher/add-question/<str:pk>', addQuestion, name='teacher-add-question'),
    path('teacher/delete-question/<str:pk>', deleteQuestion, name='teacher-delete-question'),

    
]
