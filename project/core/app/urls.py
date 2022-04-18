from django.urls import path
from .views import *

urlpatterns = [
    path('', indexPage, name='index'),

    path('student/login', studentLogin, name='student-login'),
    path('student/exam', studentExam, name='student-exam'),
    path('student/result', studentResult, name='student-result'),

    path('teacher/login', teacherLogin, name='teacher-login'),
    path('teacher/dashboard', teacherDashboard, name='teacher-dashboard'),
    
    path('teacher/subject<int:pk>', teacherSubject, name='teacher-subject'),
    path('teacher/add-subject', addSubject, name='teacher-add-subject'),
    path('teacher/all-questions<int:pk>', allQuestions, name='all-questions'),

    path('logout', logoutPage, name='logout'),
]
