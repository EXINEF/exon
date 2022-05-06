from django.http.response import Http404
from django.shortcuts import redirect

from .models import Teacher


# only the admin can see this page
def teacher_only(view_func):
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
			raise Http404
	
	return wrapper_function


def student_only(view_func):
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
			raise Http404
		else:
			return view_func(request, *args, **kwargs)
	
	return wrapper_function


# use in a NOT AUTH page ex: index page
# TODO redirect the admin to admin-page
def unauthenticated_user(view_func):
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
