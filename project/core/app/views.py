from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import Now

# Create your views here.
@unauthenticated_user
def indexPage(request):
    context = {}
    return render(request,'index.html', context)

@unauthenticated_user
def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Teacher.objects.filter(user=user).exists():
                # redirect to index, that will redirect in home or admin
                messages.error(request, 'You are a teacher, you have to log in as a teacher')
                return redirect('index')
            else:
                login(request, user)
                messages.success(request, 'Authentication as a student successful')
                return redirect('student-start-exam')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'auth/student-login.html', context)


@student_only
def studentStartExam(request):
    exam = Exam.objects.get(student=request.user)
    if exam.is_started():
        return redirect('student-exam')

    if request.method == 'POST':
        exam.start_datetime = Now()
        exam.save()
        return redirect('student-exam')

    context = {'exam':exam, }
    return render(request,'student/start-exam.html', context)

@student_only
def studentExam(request,):
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


@student_only
def studentExamQuestion(request, pk):
    exam = Exam.objects.get(student=request.user)
    if not exam.is_started():
        return redirect('student-start-exam')
    if exam.is_finished():
        return redirect('student-exam-result')
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

    context = {'exam':exam, 'questions':questions, 'main_question':main_question, 'answers_main_question':answers_main_question, }
    return render(request,'student/exam.html', context)


@student_only
def studentConfirmationFinishExam(request):
    exam = Exam.objects.get(student=request.user)

    if not exam.is_started():
        return redirect('student-start-exam')
    if exam.is_finished():
        return redirect('student-exam-result')

    if request.method == 'POST':
        messages.success(request,'Your exam was sent successfuly')
        exam.finish_datetime = Now()
        exam.save()
        return redirect('student-exam-result')

    questions = ExamQuestion.objects.filter(exam=exam).order_by('pk')
    num_questions_answer = 0
    for q in questions:
        if q.answer is not None:
            num_questions_answer += 1
    context = {'exam':exam, 'questions':questions, 'num_questions_answer':num_questions_answer, }
    return render(request,'student/confirmation-finish-exam.html', context)

@student_only
def studentNoExamAvailable(request):
    return render(request,'student/no-exam-available.html')



@student_only
def studentResult(request):
    return render(request,'student/result.html')



def logoutPage(request):
    logout(request)
    return redirect('index')

@unauthenticated_user
def teacherLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Teacher.objects.filter(user=user).exists():
                login(request, user)
                # redirect to index, that will redirect in home or admin
                messages.success(request, 'Authentication as a teacher successful')
                return redirect('teacher-dashboard')
            else:
                messages.error(request, 'You are not a teacher, Log In as a Student, to do the exam.')
                return redirect('index')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'auth/teacher-login.html', context)

def page_404(request, exception):
    return render(request, 'error/404.html')