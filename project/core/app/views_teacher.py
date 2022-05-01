from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import getAnswerValue


@login_required(login_url='index')
@teacher_only
def dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user) 
    subjects = Subject.objects.filter(teacher=teacher)

    context = {'subjects':subjects, }
    return render(request,'teacher/dashboard.html', context)




