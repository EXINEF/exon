from django.urls import path
from .views import *
from .views_teacher import dashboard

from .views_teacher_question import addQuestion, editQuestion, deleteQuestion
from .views_teacher_session import addSession, deleteSession, sessionPage, exam, sessionAllCredentials
from .views_teacher_student import addStudent, allStudents, deleteStudent, editStudent
from .views_teacher_subject import addSubject, deleteSubject, editQuestions, editSubject, loadQuestionsFile, subjectPage


urlpatterns = [
    path('', indexPage, name='index'),
    
    ### AUTH
    path('teacher/login', teacherLogin, name='teacher-login'),
    path('teacher/dashboard', dashboard, name='teacher-dashboard'),
    path('logout', logoutPage, name='logout'),
    
    ### STUDENT
    path('student/login', studentLogin, name='student-login'),
    path('student/start-exam', studentStartExam, name='student-start-exam'),
    path('student/exam', studentExam, name='student-exam'),
    path('student/exam/<str:pk>', studentExamQuestion, name='student-exam-question'),
    path('student/result', studentResult, name='student-result'),
    path('student/confirmation-finish-exam', studentConfirmationFinishExam, name='student-confiramtion-finish-exam'),
    path('student/no-exam-available', studentNoExamAvailable, name='student-no-exam-available'),


    ### TEACHER
    
    # QUESTION
    path('teacher/add-question/<str:pk>', addQuestion, name='teacher-add-question'),
    path('teacher/edit-question/<str:subjectpk>/<str:pk>', editQuestion, name='teacher-edit-question'),
    path('teacher/delete-question/<str:subjectpk>/<str:pk>', deleteQuestion, name='teacher-delete-question'),

    # SESSION
    path('teacher/session/<str:pk>', sessionPage, name='teacher-session'), 
    path('teacher/add-session/<str:pk>', addSession, name='teacher-add-session'), 
    path('teacher/delete-session/<str:pk>', deleteSession, name='teacher-delete-session'), 
    path('teacher/exam/<str:session_pk>/<str:exam_pk>', exam, name='teacher-exam'), 
    path('teacher/all-credentials/<str:pk>', sessionAllCredentials, name='teacher-all-credentials'), 

    # STUDENT
    path('teacher/add-student', addStudent, name='teacher-add-student'),
    path('teacher/all-students', allStudents, name='teacher-all-students'),
    path('teacher/delete-student/<str:pk>', deleteStudent, name='teacher-delete-student'),
    path('teacher/edit-student/<str:pk>', editStudent, name='teacher-edit-student'),

    # SUBJECT
    path('teacher/subject/<str:pk>', subjectPage, name='teacher-subject'),
    path('teacher/load-questions-file/<str:pk>', loadQuestionsFile, name='teacher-load-questions-file'),
    path('teacher/add-subject', addSubject, name='teacher-add-subject'),
    path('teacher/delete-subject/<str:pk>', deleteSubject, name='teacher-delete-subject'),
    path('teacher/edit-subject/<str:pk>', editSubject, name='teacher-edit-subject'),
    path('teacher/edit-questions/<str:pk>', editQuestions, name='teacher-edit-questions'),

    

    

    
    
]
