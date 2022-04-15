from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.
def indexPage(request):
    return render(request,'index.html')

def studentLogin(request):
    return render(request,'student/student-login.html')

def studentExam(request):
    return render(request,'student/student-exam.html')

def studentResult(request):
    return render(request,'student/student-result.html')

def teacherLogin(request):
    return render(request,'teacher/teacher-login.html')

def teacherDashboard(request):
    return render(request,'teacher/teacher-dashboard.html')

def teacherAllSubjects(request):
    subjects = Subject.objects.all()

    context = {'subjects':subjects, }
    return render(request,'teacher/teacher-all-subjects.html', context)

def teacherSubject(request, pk):
    subject = get_object_or_404(Subject, id=pk)

    context = {'subject':subject, }
    return render(request,'teacher/teacher-subject.html', context)