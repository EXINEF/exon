from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .decorators import *
from .forms import *
from .models import *
from . utils import generateUserExamQuestionsForStudent

@teacher_only
def addSession(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, id=pk, teacher=teacher)
    form = GeneralSessionForm

    if request.method == 'POST':
        form = GeneralSessionForm(request.POST)
        if form.is_valid():   
            new_session = form.save(commit=False)
            new_session.subject = subject
            new_session.teacher = teacher
            new_session.save()
            form.save_m2m()

            messages.success(request, 'New Exam Session added successful')
            return redirect('teacher-session', new_session.pk)

    context = {'subject':subject, 'form':form, }
    return render(request,'teacher/session/add-session.html', context)

@teacher_only
def editSession(request, pk):   
    teacher = get_object_or_404(Teacher, user=request.user)  
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    form = SessionForm(instance = session)
    
    if request.method == 'POST':
        form = SessionForm(request.POST, instance = session)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Session saved successfuly')
            return redirect('teacher-subject', session.subject.pk)

    context = {'form':form, 'session':session, }
    return render(request, 'teacher/session/edit-session.html', context)


@teacher_only
def editSettingsSession(request, pk):   
    teacher = get_object_or_404(Teacher, user=request.user)  
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    form = SettingsSessionForm(instance = session)
    
    if request.method == 'POST':
        form = SettingsSessionForm(request.POST, instance = session)
        
        if form.is_valid():
            
            if int(request.POST.get('number_of_questions'))>session.subject.getNumOfQuestion():
                messages.error(request, 'ERROR: there are not enough questions, asked:%s, available:%s . Load more question to the subject or decrese the number of questions for the session.' % (int(request.POST.get('number_of_questions')), session.subject.getNumOfQuestion()))
                return redirect('teacher-session', session.pk)

            form.save()
            messages.success(request, 'Session saved successfuly')
            return redirect('teacher-session', session.pk)

    context = {'form':form, 'session':session, }
    return render(request, 'teacher/session/edit-settings-session.html', context)


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



@teacher_only
def sessionPage(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    exams = session.getExams()
    num_started_exams = session.getStartedExams(exams)
    num_finished_exams = session.getFinishedExams(exams)
    accesses = Access.objects.filter()

    context = {'session':session, 'exams':exams, 'num_started_exams':num_started_exams, 'num_finished_exams':num_finished_exams, 'accesses':accesses}
    return render(request,'teacher/session/session.html', context)


@teacher_only
def exam(request, session_pk, exam_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=session_pk, teacher=teacher)
    exam = get_object_or_404(Exam, id=exam_pk, session=session)
    exam_questions = ExamQuestion.objects.filter(exam=exam)

    context = {'session':session, 'exam':exam, 'exam_questions':exam_questions}
    return render(request,'teacher/exam/exam.html', context)



@teacher_only
def sessionAllCredentials(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    exams = session.getExams()

    context = {'session':session, 'exams':exams }
    return render(request,'teacher/session/all-credentials.html', context)


@teacher_only
def generateExamsConfirmation(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    students = Student.objects.filter(session=session)
    
    if request.method == 'POST':
        messages.success(request,'The Exams for the Session: %s were created successfuly' % session.name)
        for student in students:
            generateUserExamQuestionsForStudent(session, student)

        session.is_started = True
        session.save()
        return redirect('teacher-session', session.pk)

    context = {'session':session, 'students':students, } 
    return render(request, 'teacher/session/generate-exams-confirmation.html', context)

@teacher_only
def lockSession(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    session.is_locked = True
    session.save()
    messages.warning(request,'The Session: %s is now LOCKED' % session.name)
    return redirect('teacher-session', session.pk)


@teacher_only
def unlockSession(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    session.is_locked = False
    session.save()
    messages.warning(request,'The Session: %s is now UNLOCK' % session.name)
    return redirect('teacher-session', session.pk)