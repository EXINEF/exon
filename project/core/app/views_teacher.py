from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import generateUserExamQuestionsForStudent, getAnswerValue


@login_required(login_url='index')
@teacher_only
def dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user) 
    subjects = Subject.objects.filter(teacher=teacher)

    context = {'subjects':subjects, }
    return render(request,'teacher/dashboard.html', context)

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
    return render(request, 'teacher/question/add-question.html', context)

@login_required(login_url='index')
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
                answer.is_correct = getAnswerValue(request.POST.get('is_correct'+str(c)))
                answer.save()
                c+=1
    
            messages.success(request, 'Question saved successfuly')
            return redirect('teacher-edit-questions', subjectpk)

    context = {'form':form, 'answers':answers}
    return render(request, 'teacher/question/edit-question.html', context)



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
    return render(request, 'teacher/question/delete-question.html', context)


@login_required(login_url='index')
@teacher_only
def addStudent(request):   
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            t = Teacher.objects.get(user=request.user)     
            new_student = form.save(commit=False)
            if Student.objects.filter(teacher=t, matricola=new_student.matricola).exists(): 
                messages.error(request, 'STUDENT WITH THIS MATRICOLA CODE ALREADY EXISTS')
                return redirect('teacher-dashboard')
            new_student.teacher = t
            new_student.save()
            form.save_m2m()

            messages.success(request, 'New Student %s added successful' % (new_student.__str__()))
            return redirect('teacher-dashboard')

    context = {'form':form}
    return render(request, 'teacher/student/add-student.html', context)

@login_required(login_url='index')
@teacher_only
def allStudents(request):   
    teacher = get_object_or_404(Teacher, user=request.user)
    students = Student.objects.filter(teacher=teacher)

    context = {'students':students}
    return render(request, 'teacher/student/all-students.html', context)
