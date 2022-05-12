from django.contrib import messages
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404, render

from .decorators import *
from .forms import *
from .models import *


@student_only
def student_start_exam(request):
	exam = Exam.objects.get(student=request.user)
	if not exam.session.is_open():
		return redirect('student-exam-error')
	
	if exam.is_started():
		return redirect('student-exam')
	
	if request.method == 'POST':
		exam.set_started()
		exam.save()
		return redirect('student-exam')
	
	context = {'exam': exam, }
	return render(request, 'student/start-exam.html', context)


@student_only
def student_exam(request, ):
	exam = Exam.objects.get(student=request.user)
	if not exam.is_started():
		return redirect('student-start-exam')
	
	if exam.is_finished():
		return redirect('student-exam-result')
	
	questions = ExamQuestion.objects.filter(exam=exam).order_by('pk')
	for q in questions:
		if q.answer is None:
			return redirect('student-exam-question', q.pk)
	return redirect('student-exam-question', questions[0].pk)


def student_exam_time_expired(request):
	return render(request, 'student/exam-time-expired.html')


@student_only
def student_exam_question(request, pk):
	exam = Exam.objects.get(student=request.user)
	if not exam.is_started():
		return redirect('student-start-exam')
	if exam.is_finished():
		return redirect('student-exam-result')
	
	if exam.isExpired():
		exam.finish_datetime = Now()
		exam.analyzeExam()
		exam.save()
		return redirect('student-exam-time-expired')
	
	main_question = get_object_or_404(ExamQuestion, id=pk)
	answers_main_question = Answer.objects.filter(question=main_question.question)
	questions = ExamQuestion.objects.filter(exam=exam).order_by('pk')
	
	if request.method == 'POST':
		for answer in answers_main_question:
			
			if int(request.POST.get('answer')) == answer.id:
				main_question.answer = answer
				break
		
		main_question.save()
		return redirect('student-exam')
	
	context = {'exam': exam, 'questions': questions, 'main_question': main_question,
	           'answers_main_question': answers_main_question, }
	return render(request, 'student/exam.html', context)


@student_only
def student_confirmation_finish_exam(request):
	exam = Exam.objects.get(student=request.user)
	
	if not exam.is_started():
		return redirect('student-start-exam')
	if exam.is_finished():
		return redirect('student-exam-result')
	
	if request.method == 'POST':
		messages.success(request, 'Your exam was sent successfuly')
		exam.set_finished()
		exam.save()
		return redirect('student-exam-result')
	
	questions = ExamQuestion.objects.filter(exam=exam).order_by('pk')
	num_questions_answer = 0
	for q in questions:
		if q.answer is not None:
			num_questions_answer += 1
	context = {'exam': exam, 'questions': questions, 'num_questions_answer': num_questions_answer, }
	return render(request, 'student/confirmation-finish-exam.html', context)


@student_only
def student_exam_error(request):
	exam = Exam.objects.get(student=request.user)
	if exam.session.is_open() and not exam.is_started():
		return redirect('student-start-exam')
	context = {'exam': exam, }
	return render(request, 'student/exam-error.html', context)


@student_only
def student_result(request):
	exam = Exam.objects.get(student=request.user)
	questions = ExamQuestion.objects.filter(exam=exam)
	answersList = []
	for q in questions:
		answers = Answer.objects.filter(question=q.question)
		answersList.append(answers)
	
	if not exam.is_started():
		return redirect('student-start-exam')
	if not exam.is_finished():
		return redirect('student-exam')
	
	context = {'exam': exam, 'questions': questions, 'answersList': answersList, }
	return render(request, 'student/result.html', context)