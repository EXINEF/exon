from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from .decorators import *


# Create your views here.
@unauthenticated_user
def indexPage(request):
	context = {}
	return render(request, 'index.html', context)


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
	return render(request, 'auth/student-login.html', context)


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
	return render(request, 'auth/teacher-login.html', context)


def page_404(request, exception):
	return render(request, 'error/404.html')
