from django.urls import path
from .views import *

from .views_student import *
from .views_teacher import dashboard
from .views_teacher_question import add_question, edit_question, delete_question
from .views_teacher_session import *
from .views_teacher_student import add_student, load_file_students, all_students, delete_student, edit_student
from .views_teacher_subject import add_subject, delete_subject, edit_questions, edit_subject, load_questions_file, subject_page

urlpatterns = [
	path('', indexPage, name='index'),
	
	### AUTH
	path('teacher/login', teacher_login, name='teacher-login'),
	path('teacher/dashboard', dashboard, name='teacher-dashboard'),
	path('logout', logout_page, name='logout'),
	
	### STUDENT
	path('student/login', student_login, name='student-login'),
	path('student/start-exam', student_start_exam, name='student-start-exam'),
	path('student/exam', student_exam, name='student-exam'),
	path('student/exam/<str:pk>', student_exam_question, name='student-exam-question'),
	path('student/exam-result', student_result, name='student-exam-result'),
	path('student/confirmation-finish-exam', student_confirmation_finish_exam, name='student-confiramtion-finish-exam'),
	path('student/exam-error', student_exam_error, name='student-exam-error'),
	path('student/student-exam-time-expired', student_exam_time_expired, name='student-exam-time-expired'),
	
	### TEACHER
	
	# QUESTION
	path('teacher/add-question/<str:pk>', add_question, name='teacher-add-question'),
	path('teacher/edit-question/<str:subjectpk>/<str:pk>', edit_question, name='teacher-edit-question'),
	path('teacher/delete-question/<str:subjectpk>/<str:pk>', delete_question, name='teacher-delete-question'),
	
	# SESSION
	path('teacher/session/<str:pk>', session_page, name='teacher-session'),
	path('teacher/add-session/<str:pk>', add_session, name='teacher-add-session'),
	path('teacher/edit-session/<str:pk>', edit_session, name='teacher-edit-session'),
	path('teacher/edit-settings-session/<str:pk>', edit_settings_session, name='teacher-edit-settings-session'),
	path('teacher/edit-weights-session/<str:pk>', edit_weights_session, name='teacher-edit-weights-session'),
	path('teacher/delete-session/<str:pk>', delete_session, name='teacher-delete-session'),
	path('teacher/exam/<str:session_pk>/<str:exam_pk>', exam, name='teacher-exam'),
	path('teacher/all-credentials/<str:pk>', session_all_credentials, name='teacher-all-credentials'),
	path('teacher/generate-exams-confirmation/<str:pk>', generate_exams_confirmation, name='teacher-generate-exams-confirmation'),
	path('teacher/terminate-session-confirmation/<str:pk>', terminate_session_confirmation, name='teacher-terminate-session-confirmation'),
	path('teacher/lock-session/<str:pk>', lock_session, name='teacher-lock-session'),
	path('teacher/unlock-session/<str:pk>', unlock_session, name='teacher-unlock-session'),
	path('teacher/correct-exams/<str:pk>', correct_exams, name='teacher-correct-exams'),
	path('teacher/export-exam-pdf/<str:session_pk>/<str:exam_pk>', export_exam_pdf, name='teacher-export-exam-pdf'),

	# STUDENT
	path('teacher/add-student/<str:pk>', add_student, name='teacher-add-student'),
	path('teacher/load-file-students/<str:pk>', load_file_students, name='teacher-load-file-students'),
	path('teacher/all-students/<str:pk>', all_students, name='teacher-all-students'),
	path('teacher/delete-student/<str:session_pk>/<str:student_pk>', delete_student, name='teacher-delete-student'),
	path('teacher/edit-student/<str:session_pk>/<str:student_pk>', edit_student, name='teacher-edit-student'),
	
	# SUBJECT
	path('teacher/subject/<str:pk>', subject_page, name='teacher-subject'),
	path('teacher/load-questions-file/<str:pk>', load_questions_file, name='teacher-load-questions-file'),
	path('teacher/add-subject', add_subject, name='teacher-add-subject'),
	path('teacher/delete-subject/<str:pk>', delete_subject, name='teacher-delete-subject'),
	path('teacher/edit-subject/<str:pk>', edit_subject, name='teacher-edit-subject'),
	path('teacher/edit-questions/<str:pk>', edit_questions, name='teacher-edit-questions'),

]
