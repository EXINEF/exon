from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .decorators import *
from .forms import *
from .utils import get_answer_value


@teacher_only
def add_question(request, pk):
    form = QuestionForm()
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.teacher = teacher
            new_question.subject = subject
            new_question.save()
            form.save_m2m()
            
            for i in range(4):
                text = request.POST.get('answer' + str(i))
                answer = Answer()
                answer.text = text
                answer.question = new_question
                answer.teacher = teacher
                answer.is_correct = get_answer_value(request.POST.get('is_correct'+str(i)))
                answer.save()

            messages.success(request, 'New question added successful')
            return redirect('teacher-edit-questions', pk, 0 ,5)
    
    context = {'form': form, 'range': range(4), 'subject': subject}
    return render(request, 'teacher/question/add-question.html', context)


@teacher_only
def edit_question(request, subjectpk, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    question = get_object_or_404(Question, id=pk, teacher=teacher)
    answers = get_list_or_404(Answer, question=question)
    form = QuestionForm(instance=question)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        
        if form.is_valid():
            form.save()
            c = 1
            for answer in answers:
                text = request.POST.get('answer' + str(c))
                answer.text = text
                answer.is_correct = get_answer_value(request.POST.get('is_correct'+str(c)))
                answer.save()
                c += 1

            c = 1

            messages.success(request, 'Question saved successfully')
            return redirect('teacher-edit-questions', subjectpk, 0 ,5)
    
    context = {'form': form, 'answers': answers}
    return render(request, 'teacher/question/edit-question.html', context)


@teacher_only
def delete_question(request, subjectpk, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    question = get_object_or_404(Question, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request, 'The Question %s was deleted successfuly' % question.text)
        Question.delete(question)
        return redirect('teacher-edit-questions', subjectpk, 0 ,5)
    
    context = {'question': question}
    return render(request, 'teacher/question/delete-question.html', context)
