from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@unauthenticated_user
def indexPage(request):
    context = {}
    return render(request,'index.html', context)

def studentLogin(request):
    return render(request,'student/login.html')

def studentExam(request):
    return render(request,'student/exam.html')

def studentResult(request):
    return render(request,'student/result.html')

@unauthenticated_user
def teacherLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # redirect to index, that will redirect in home or admin
            messages.success(request, 'Authentication successful')
            return redirect('teacher-dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'teacher/login.html', context)

def teacherDashboard(request):
    subjects = Subject.objects.all()

    context = {'subjects':subjects, }
    return render(request,'teacher/dashboard.html', context)

def teacherSubject(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    num_questions = Question.objects.filter(subject=subject).count()
    context = {'subject':subject, 'num_questions':num_questions }
    return render(request,'teacher/subject.html', context)

@login_required(login_url='index')
@teacher_only
def addSubject(request):   
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            t = Teacher.objects.get(user=request.user)     
            new_subject = form.save(commit=False)
            new_subject.teacher = t
            new_subject.save()
            form.save_m2m()

            messages.success(request, 'New subject added successful')
            return redirect('teacher-dashboard')

    context = {'form':form}
    return render(request, 'teacher/add-subject.html', context)

@login_required(login_url='index')
def logoutPage(request):
    logout(request)
    return redirect('index')

def allQuestions(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    questions = Question.objects.filter(subject = subject)
    context = {'subject':subject, 'questions' : questions}
    return render(request,'teacher/all-questions.html', context)