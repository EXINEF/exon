from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from .utils import generateUserExamQuestionsForStudent, getAnswerValue


@login_required(login_url='index')
@teacher_only
def addSession(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)
    students = Student.objects.filter(teacher=teacher)

    form = SessionForm()
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():   
            new_session = form.save(commit=False)
            if new_session.number_of_questions>subject.getNumOfQuestion():
                messages.error(request, 'ERROR: there are not enough questions, asked:%s, available:%s' % (new_session.number_of_questions, subject.getNumOfQuestion()))
                return redirect('teacher-subject', subject.id)
            new_session.subject = subject
            new_session.teacher = teacher
            new_session.save()
            form.save_m2m()

            for student in students:
                
                if request.POST.get(student.matricola) == '1':
                    generateUserExamQuestionsForStudent(new_session,student)

            messages.success(request, 'New Exam Session added successful')
            return redirect('teacher-subject', subject.id)

    context = {'subject':subject, 'form':form, 'students':students}
    return render(request,'teacher/session/add-session.html', context)


@login_required(login_url='index')
@teacher_only
def deleteSession(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request,'The Session Exam %s was deleted successfuly' % session.getName())
        exams = Exam.objects.filter(session=session)
        for exam in exams:
            User.delete(exam.student)
        Session.delete(session)

        return redirect('teacher-subject', session.subject.id)

    context = {'session':session} 
    return render(request, 'teacher/session/delete-session.html', context)


@login_required(login_url='index')
@teacher_only
def session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    exams = session.getExams()
    num_started_exams = session.getStartedExams(exams)
    num_finished_exams = session.getFinishedExams(exams)

    context = {'session':session, 'exams':exams, 'num_started_exams':num_started_exams, 'num_finished_exams':num_finished_exams}
    return render(request,'teacher/session/session.html', context)

@login_required(login_url='index')
@teacher_only
def exam(request, session_pk, exam_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=session_pk, teacher=teacher)
    exam = get_object_or_404(Exam, id=exam_pk, session=session)
    exam_questions = ExamQuestion.objects.filter(exam=exam)

    context = {'session':session, 'exam':exam, 'exam_questions':exam_questions}
    return render(request,'teacher/exam/exam.html', context)
