from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .decorators import *
from .forms import *


@login_required(login_url='index')
@teacher_only
def dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user) 
    subjects = Subject.objects.filter(teacher=teacher)

    context = {'subjects':subjects, }
    return render(request, 'teacher/dashboard.html', context)

def personal_area(request):
    teacher = get_object_or_404(Teacher, user=request.user) 

    context = {'teacher':teacher, }
    return render(request, 'teacher/settings/personal-area.html', context)


