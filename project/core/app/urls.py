from django.urls import path
from .views import *

from .views_student import *
from .views_teacher import dashboard
from .views_teacher_question import addQuestion, editQuestion, deleteQuestion
from .views_teacher_session import *
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
	path('student/exam-result', studentResult, name='student-exam-result'),
	path('student/confirmation-finish-exam', studentConfirmationFinishExam, name='student-confiramtion-finish-exam'),
	path('student/exam-error', studentExamError, name='student-exam-error'),
	path('student/student-exam-time-expired', studentExamTimeExpired, name='student-exam-time-expired'),
	
	### TEACHER
	
	# QUESTION
	path('teacher/add-question/<str:pk>', addQuestion, name='teacher-add-question'),
	path('teacher/edit-question/<str:subjectpk>/<str:pk>', editQuestion, name='teacher-edit-question'),
	path('teacher/delete-question/<str:subjectpk>/<str:pk>', deleteQuestion, name='teacher-delete-question'),
	
	# SESSION
	path('teacher/session/<str:pk>', sessionPage, name='teacher-session'),
	path('teacher/add-session/<str:pk>', addSession, name='teacher-add-session'),
	path('teacher/edit-session/<str:pk>', editSession, name='teacher-edit-session'),
	path('teacher/edit-settings-session/<str:pk>', editSettingsSession, name='teacher-edit-settings-session'),
	path('teacher/delete-session/<str:pk>', deleteSession, name='teacher-delete-session'),
	path('teacher/exam/<str:session_pk>/<str:exam_pk>', exam, name='teacher-exam'),
	path('teacher/all-credentials/<str:pk>', sessionAllCredentials, name='teacher-all-credentials'),
	path('teacher/generate-exams-confirmation/<str:pk>', generateExamsConfirmation, name='teacher-generate-exams-confirmation'),
	path('teacher/lock-session/<str:pk>', lockSession, name='teacher-lock-session'),
	path('teacher/unlock-session/<str:pk>', unlockSession, name='teacher-unlock-session'),

	# STUDENT
	path('teacher/add-student/<str:pk>', addStudent, name='teacher-add-student'),
	path('teacher/all-students/<str:pk>', allStudents, name='teacher-all-students'),
	path('teacher/delete-student/<str:session_pk>/<str:student_pk>', deleteStudent, name='teacher-delete-student'),
	path('teacher/edit-student/<str:session_pk>/<str:student_pk>', editStudent, name='teacher-edit-student'),
	
	# SUBJECT
	path('teacher/subject/<str:pk>', subjectPage, name='teacher-subject'),
	path('teacher/load-questions-file/<str:pk>', loadQuestionsFile, name='teacher-load-questions-file'),
	path('teacher/add-subject', addSubject, name='teacher-add-subject'),
	path('teacher/delete-subject/<str:pk>', deleteSubject, name='teacher-delete-subject'),
	path('teacher/edit-subject/<str:pk>', editSubject, name='teacher-edit-subject'),
	path('teacher/edit-questions/<str:pk>', editQuestions, name='teacher-edit-questions'),

]
