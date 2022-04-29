
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .utils import generateNExamsForSession

@login_required(login_url='index')
@teacher_only
def dashboard(request):
    subjects = Subject.objects.all()

    context = {'subjects':subjects, }
    return render(request,'teacher/dashboard.html', context)

@login_required(login_url='index')
@teacher_only
def subject(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    subject = get_object_or_404(Subject, id=pk)
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
    return render(request, 'teacher/subject/edit-subject.html', context)

@login_required(login_url='index')
@teacher_only
def editQuestions(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    questions = Question.objects.filter(subject = subject)
    context = {'subject':subject, 'questions' : questions}
    return render(request,'teacher/subject/edit-questions.html', context)

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
    return render(request, 'teacher/question/edit-question.html', context)

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
    return render(request, 'teacher/question/delete-question.html', context)

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

            students = request.POST.get('students')
            #TODO select a way to insert students in the session
            # TODO select a way to display students to add in add session
            # TODO so that is not too difficult to insert them
            # TODO CONNECT TO THE BACK END and create exam with unique users for each student
            print('QUE LO QUE'+students)

            #generateNExamsForSession(new_session)

            

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
        messages.success(request,'The Session Exam %s was deleted successfuly' % session.start_datetime)
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
    session = get_object_or_404(Session, id=session_pk)
    exam = get_object_or_404(Exam, id=exam_pk, session=session)
    exam_questions = ExamQuestion.objects.filter(exam=exam)

    context = {'session':session, 'exam':exam, 'exam_questions':exam_questions}
    return render(request,'teacher/exam/exam.html', context)

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
