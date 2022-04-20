
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='index')
@teacher_only
def dashboard(request):
    subjects = Subject.objects.all()

    context = {'subjects':subjects, }
    return render(request,'teacher/dashboard.html', context)

@login_required(login_url='index')
@teacher_only
def subject(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    num_questions = Question.objects.filter(subject=subject).count()
    context = {'subject':subject, 'num_questions':num_questions }
    return render(request,'teacher/subject.html', context)

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
    return render(request, 'teacher/add-subject.html', context)

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
    return render(request, 'teacher/delete-subject.html', context)

@login_required(login_url='index')
@teacher_only
def editQuestions(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    questions = Question.objects.filter(subject = subject)
    context = {'subject':subject, 'questions' : questions}
    return render(request,'teacher/edit-questions.html', context)

@login_required(login_url='index')
@teacher_only
def addQuestion(request, pk):   
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            t = get_object_or_404(Teacher, user=request.user)  
            s = get_object_or_404(Subject, id=pk)
            new_question = form.save(commit=False)
            new_question.teacher = t
            new_question.subject = s
            new_question.save()
            form.save_m2m()
            for i in range(4):
                text = request.POST.get('answer'+str(i))
                answer = Answer()
                answer.text = text
                answer.question = new_question
                answer.teacher = t
                answer.is_correct = getAnswerValue(request.POST.get('is_correct'+str(i)))
                answer.save()
    
            messages.success(request, 'New question added successful')
            return redirect('teacher-edit-questions', pk)

    context = {'form':form, 'range':range(4),}
    return render(request, 'teacher/add-question.html', context)

@login_required(login_url='index')
@teacher_only
def editQuestion(request, subjectpk, pk):   
    t = get_object_or_404(Teacher, user=request.user)  
    question = get_object_or_404(Question, id=pk, teacher=t)
    answers = get_list_or_404(Answer, question=question)
    form = QuestionForm(instance = question)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance = question)
        
        if form.is_valid():
            form.save()
            c = 1
            for answer in answers:
                text = request.POST.get('answer'+str(c))
                answer.text = text
                answer.is_correct = getAnswerValue(request.POST.get('is_correct'+str(c)))
                answer.save()
                c+=1
    
            messages.success(request, 'Question saved successfuly')
            return redirect('teacher-edit-questions', subjectpk)

    context = {'form':form, 'answers':answers}
    return render(request, 'teacher/edit-question.html', context)

def getAnswerValue(value):
    if value is None:
        return 0
    return 1

@login_required(login_url='index')
@teacher_only
def deleteQuestion(request, subjectpk, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    question = get_object_or_404(Question, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request,'The Question %s was deleted successfuly' % question.text)
        Question.delete(question)
        return redirect('teacher-edit-questions', subjectpk)

    context = {'question':question}
    return render(request, 'teacher/delete-question.html', context)

@login_required(login_url='index')
@teacher_only
def editSubject(request, pk):   
    t = get_object_or_404(Teacher, user=request.user)  
    subject = get_object_or_404(Subject, id=pk, teacher=t)

    form = SubjectForm(instance = subject)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance = subject)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject saved successfuly')
            return redirect('teacher-dashboard')

    context = {'form':form,}
    return render(request, 'teacher/edit-subject.html', context)