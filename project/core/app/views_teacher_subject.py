from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import generateUserExamQuestionsForStudent, getAnswerValue


@login_required(login_url='index')
@teacher_only
def subject(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)
    num_questions = Question.objects.filter(subject=subject).count()
    sessions = Session.objects.filter(subject=subject, teacher=teacher)

    context = {'subject':subject, 'num_questions':num_questions, 'sessions':sessions}
    return render(request,'teacher/subject/subject.html', context)


@login_required(login_url='index')
@teacher_only
def loadQuestionsFile(request, pk):
    context = {}
    return render(request,'teacher/subject/load-questions-file.html', context)


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
    return render(request, 'teacher/subject/add-subject.html', context)

@login_required(login_url='index')
@teacher_only
def deleteSubject(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request,'The Subject %s was deleted successfuly' % subject.name)
        Subject.delete(subject)
        return redirect('teacher-dashboard')

    context = {'subject':subject}
    return render(request, 'teacher/subject/delete-subject.html', context)

@login_required(login_url='index')
@teacher_only
def editSubject(request, pk):   
    teacher = get_object_or_404(Teacher, user=request.user)  
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)

    form = SubjectForm(instance = subject)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance = subject)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject saved successfuly')
            return redirect('teacher-dashboard')

    context = {'form':form,}
    return render(request, 'teacher/subject/edit-subject.html', context)

@login_required(login_url='index')
@teacher_only
def editQuestions(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)  
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)
    questions = Question.objects.filter(subject = subject)
    context = {'subject':subject, 'questions' : questions}
    return render(request,'teacher/subject/edit-questions.html', context)
