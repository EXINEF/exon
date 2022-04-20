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

@login_required(login_url='index')
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
            login(request, user)
            # redirect to index, that will redirect in home or admin
            messages.success(request, 'Authentication successful')
            return redirect('teacher-dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request,'teacher/login.html', context)

def page_404(request, exception):
    return render(request, 'error/404.html')