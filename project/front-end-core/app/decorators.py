from django.http.response import Http404
from django.shortcuts import redirect, HttpResponse
from .models import Teacher

# only the admin can see this page
def teacher_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admin')
    
        t = Teacher.objects.get(user=request.user)
        if t is not None:
            return view_func(request, *args, **kwargs)      
        else:
            raise Http404
    return wrapper_function

# use in a NOT AUTH page ex: index page
# TODO redirect the admin to admin-page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/admin')

            t = Teacher.objects.get(user=request.user)
            if t is not None:
                return redirect('teacher-dashboard')   
            else:
                return HttpResponse('You are a student')		
        
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func