from django.http.response import Http404
from django.shortcuts import redirect

from .models import Teacher

"""
	DECORATORS allow to excecute actions before start a function in views,
	in this case we used to make a sensitive page inacessible to an unathorized user,
	instead of checking in each function
"""


def teacher_only(view_func):
	"""
		Check if the current user is logged in and is a teacher,

		if TRUE it shows that page,
		else redirect to index page
	"""
	def wrapper_function(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		
		if request.user.is_staff:
			return redirect('/admin')
		
		try:
			t = Teacher.objects.get(user=request.user)
		
		except Teacher.DoesNotExist:
			t = None
		
		if t is not None:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('index')
	
	return wrapper_function


def student_only(view_func):
	"""
		Check if the current user is logged in and is a student,

		if TRUE it shows that page,
		else redirect to index page
	"""
	def wrapper_function(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('index')
		
		if request.user.is_staff:
			return redirect('/admin')
		try:
			t = Teacher.objects.get(user=request.user)
		except Teacher.DoesNotExist:
			t = None
		if t is None:
			return view_func(request, *args, **kwargs)	
		else:
			return redirect('index')
	
	return wrapper_function


def unauthenticated_user(view_func):
	"""
		Check if the current user is NOT logged in

		if TRUE it shows that page,
		else redirect to teacher or student main pages
	"""
	def wrapper_func(request, *args, **kwargs):
		
		if request.user.is_authenticated:
			if request.user.is_staff:
				return redirect('/admin')
			
			try:
				t = Teacher.objects.get(user=request.user)
			
			except Teacher.DoesNotExist:
				t = None
			
			if t is not None:
				return redirect('teacher-dashboard')
			else:
				return redirect('student-start-exam')
		
		else:
			return view_func(request, *args, **kwargs)
	
	return wrapper_func
