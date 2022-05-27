from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .decorators import *
from .forms import *
from .models import *
from .utils import select_random_question_poll_from_subject, generate_user_and_exam_for_student, send_token_by_email_for_exam


@teacher_only
def add_session(request, pk):
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
def edit_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)  
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['READY','FINISHED']):
        return redirect('teacher-session', session.pk)

    form = SessionForm(instance = session)
    
    if request.method == 'POST':
        form = SessionForm(request.POST, instance = session)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Session saved successfuly')
            return redirect('teacher-session', session.pk)

    context = {'form':form, 'session':session, }
    return render(request, 'teacher/session/edit-session.html', context)


@teacher_only
def edit_settings_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)  
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['MISSING CONFIGURATION','READY']):
        return redirect('teacher-session', session.pk)

    form = SettingsSessionForm(instance = session)
    
    if request.method == 'POST':
        form = SettingsSessionForm(request.POST, instance = session)
        
        if form.is_valid():
            
            if int(request.POST.get('number_of_questions'))>session.subject.get_number_of_questions():
                messages.error(request, 'ERROR: there are not enough questions, asked:%s, available:%s . Load more question to the subject or decrese the number of questions for the session.' % (int(request.POST.get('number_of_questions')), session.subject.get_number_of_questions()))
                return redirect('teacher-session', session.pk)

            form.save()
            messages.success(request, 'Session saved successfuly')
            return redirect('teacher-session', session.pk)

    context = {'form':form, 'session':session, }
    return render(request, 'teacher/session/edit-settings-session.html', context)


@teacher_only
def edit_weights_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)  
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['FINISHED']):
        return redirect('teacher-session', session.pk)

    form = WeightsSessionForm(instance = session)
    
    if request.method == 'POST':
        form = WeightsSessionForm(request.POST, instance = session)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Session saved successfuly')
            return redirect('teacher-session', session.pk)

    context = {'form':form, 'session':session, }
    return render(request, 'teacher/session/edit-weights-session.html', context)


@teacher_only
def delete_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    
    if not session.allowed_status(['MISSING CONFIGURATION','READY','FINISHED']):
        return redirect('teacher-session', session.pk)

    if request.method == 'POST':
        messages.success(request,'The Session Exam %s was deleted successfuly' % session.name)
        exams = Exam.objects.filter(session=session)
        for exam in exams:
            User.delete(exam.student)
        Session.delete(session)
        return redirect('teacher-subject', session.subject.id)

    context = {'session':session} 
    return render(request, 'teacher/session/delete-session.html', context)


@teacher_only
def session_page(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    exams = session.get_exams()
    num_started_exams = session.get_started_exams(exams)
    num_finished_exams = session.get_finished_exams(exams)
    accesses = Access.objects.filter(session=session)

    context = {'session':session, 'exams':exams, 'num_started_exams':num_started_exams, 'num_finished_exams':num_finished_exams, 'accesses':accesses}
    return render(request,'teacher/session/session.html', context)


@teacher_only
def exam(request, session_pk, exam_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=session_pk, teacher=teacher)
    
    if not session.allowed_status(['FINISHED']):
        return redirect('teacher-session', session.pk)

    exam = get_object_or_404(Exam, id=exam_pk, session=session)
    questions = ExamQuestion.objects.filter(exam=exam)

    context = {'session':session, 'exam':exam, 'questions':questions}
    return render(request,'teacher/exam/exam.html', context)


@teacher_only
def session_all_credentials(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    exams = session.get_exams()

    context = {'session':session, 'exams':exams }
    return render(request,'teacher/session/all-credentials.html', context)


@teacher_only
def generate_exams_confirmation(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['READY']):
        return redirect('teacher-session', session.pk)

    students = Student.objects.filter(session=session)
    
    if request.method == 'POST':
        questions_poll = select_random_question_poll_from_subject(session.subject,session.number_of_questions)

        for student in students:
            generate_user_and_exam_for_student(session, student, questions_poll)

        session.is_started = True
        session.save()

        messages.success(request,'The Exams for the Session: %s were created successfuly' % session.name)
        return redirect('teacher-session', session.pk)

    context = {'session':session, 'students':students, } 
    return render(request, 'teacher/session/generate-exams-confirmation.html', context)


@teacher_only
def terminate_session_confirmation(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    if request.method == 'POST':
        session.set_finished()
        session.save()

        messages.success(request,'The Exam\'s Session: %s was terminated successfuly' % session.name)
        return redirect('teacher-session', session.pk)

    context = {'session':session, } 
    return render(request, 'teacher/session/terminate-session-confirmation.html', context)


@teacher_only
def lock_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    session.is_locked = True
    session.save()
    messages.warning(request,'The Session: %s is now LOCKED' % session.name)
    return redirect('teacher-session', session.pk)


@teacher_only
def unlock_session(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    session.is_locked = False
    session.save()
    messages.warning(request,'The Session: %s is now UNLOCK' % session.name)
    return redirect('teacher-session', session.pk)


@teacher_only
def correct_exams(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if not session.allowed_status(['FINISHED']):
        return redirect('teacher-session', session.pk)

    exams = Exam.objects.filter(session=session)
    
    for exam in exams:
        exam.analyze_and_correct_exam()
        exam.save()

    messages.success(request,'All the Exams of the Session: %s were corrected.' % session.name)
    return redirect('teacher-session', session.pk)

@teacher_only
def export_exam_pdf(request, session_pk, exam_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, pk=session_pk, teacher=teacher)

    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    exam = Exam.objects.get(pk=exam_pk)
    questions = ExamQuestion.objects.filter(exam=exam)
    answersList = []
    for q in questions:
        answers = Answer.objects.filter(question=q.question)
        answersList.append(answers)

    context = {'session':session, 'exam': exam, 'questions': questions, 'answersList': answersList, }
    
    response = HttpResponse(content_type='application/pdf')
    file_name = '\'filename=EXAM_' + str(session.pk) + '_' + exam.token + '\''
    response['Content-Disposition'] = file_name
    template = get_template('teacher/session/export-exams-pdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('ERROR: writing the pdf')
    return response


@teacher_only
def send_tokens_by_email(request, session_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, pk=session_pk, teacher=teacher)
    
    if not session.allowed_status(['STARTED']):
        return redirect('teacher-session', session.pk)

    exams = Exam.objects.filter(session=session)

    for exam in exams:
        send_token_by_email_for_exam(session, exam)

    messages.success(request,'All the Tokens of the Session: %s were sent by email to the students.' % session.name)
    return redirect('teacher-session', session.pk)