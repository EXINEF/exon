from django.urls import path
from .views import *
from .views_teacher import *

urlpatterns = [
    path('', indexPage, name='index'),
    
    # AUTH
    path('teacher/login', teacherLogin, name='teacher-login'),
    path('teacher/dashboard', dashboard, name='teacher-dashboard'),
    path('logout', logoutPage, name='logout'),
    
    # STUDENT
    path('student/login', studentLogin, name='student-login'),
    path('student/exam', studentExam, name='student-exam'),
    path('student/result', studentResult, name='student-result'),

    # TEACHER
    # SUBJECT
    path('teacher/subject/<str:pk>', subject, name='teacher-subject'),
    path('teacher/load-questions-file/<str:pk>', loadQuestionsFile, name='teacher-load-questions-file'),
    path('teacher/add-subject', addSubject, name='teacher-add-subject'),
    path('teacher/delete-subject/<str:pk>', deleteSubject, name='teacher-delete-subject'),
    path('teacher/edit-subject/<str:pk>', editSubject, name='teacher-edit-subject'),
    path('teacher/edit-questions/<str:pk>', editQuestions, name='teacher-edit-questions'),

    # QUESTION
    path('teacher/add-question/<str:pk>', addQuestion, name='teacher-add-question'),
    path('teacher/edit-question/<str:subjectpk>/<str:pk>', editQuestion, name='teacher-edit-question'),
    path('teacher/delete-question/<str:subjectpk>/<str:pk>', deleteQuestion, name='teacher-delete-question'),


    # SESSION
    path('teacher/session/<str:pk>', session, name='teacher-session'), 
    path('teacher/add-session/<str:pk>', addSession, name='teacher-add-session'), 
    path('teacher/delete-session/<str:pk>', deleteSession, name='teacher-delete-session'), 
    path('teacher/exam/<str:session_pk>/<str:exam_pk>', exam, name='teacher-exam'), 
    
]
