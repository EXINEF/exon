from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import getAnswerValue



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
                answer.is_correct = int(request.POST.get('answer')) == i
                answer.save()
    
            messages.success(request, 'New question added successful')
            return redirect('teacher-edit-questions', pk)

    context = {'form':form, 'range':range(4),}
    return render(request, 'teacher/question/add-question.html', context)


@teacher_only
def editQuestion(request, subjectpk, pk):   
    teacher = get_object_or_404(Teacher, user=request.user)  
    question = get_object_or_404(Question, id=pk, teacher=teacher)
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
                answer.is_correct = int(request.POST.get('answer')) == c
                answer.save()
                c+=1
    
            messages.success(request, 'Question saved successfuly')
            return redirect('teacher-edit-questions', subjectpk)

    context = {'form':form, 'answers':answers}
    return render(request, 'teacher/question/edit-question.html', context)




@teacher_only
def deleteQuestion(request, subjectpk, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    question = get_object_or_404(Question, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request,'The Question %s was deleted successfuly' % question.text)
        Question.delete(question)
        return redirect('teacher-edit-questions', subjectpk)

    context = {'question':question}
    return render(request, 'teacher/question/delete-question.html', context)


