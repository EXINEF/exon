from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import Exam, Access
from .decorators import *
from .utils import get_client_ip


# Create your views here.
@unauthenticated_user
def indexPage(request):
	context = {}
	return render(request, 'index.html', context)


@unauthenticated_user
def student_login(request):
	if request.method == 'POST':
		token = request.POST.get('token')
		
		user = authenticate(request, username=token, password=token)
		
		if user is not None:
			if Teacher.objects.filter(user=user).exists():
				# redirect to index, that will redirect in home or admin
				messages.error(request, 'You are a teacher, you have to log in as a teacher')
				return redirect('index')
			else:
				if not Exam.objects.filter(token=token).exists():
					messages.error(request, 'You don\'t have an exam associated with this account please, tell this to the teacher.')
					return redirect('index')

				exam = Exam.objects.get(student=user)
				if exam.session.is_locked:
					messages.error(request, 'ERROR: The session you are trying to Login is LOCKED, ask to the teacher to unlock it.')
					return redirect('student-login')
				
				login(request, user)
				
				if exam is not None:
					access = Access(session=exam.session, exam=exam, ip = get_client_ip(request))
					access.save()
				messages.success(request, 'Authentication as a student successful')
				return redirect('student-start-exam')
		else:
			messages.error(request, 'Username OR password is incorrect')
	
	context = {}
	return render(request, 'auth/student-login.html', context)


def logout_page(request):
	logout(request)
	return redirect('index')


@unauthenticated_user
def teacher_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			if Teacher.objects.filter(user=user).exists():
				login(request, user)
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
