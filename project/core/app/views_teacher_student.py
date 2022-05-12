from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .decorators import *
from .forms import *


@teacher_only
def all_students(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)
    students = Student.objects.filter(session=session)

    context = {'students':students, 'session':session}
    return render(request, 'teacher/student/all-students.html', context)


@teacher_only
def add_student(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():   
            new_student = form.save(commit=False)
            if Student.objects.filter(session=session, matricola=new_student.matricola).exists(): 
                messages.error(request, 'ERROR: a student with this matricola( %s ) already exist in this session.' % (new_student.matricola))
                return redirect('teacher-all-students', session.id)
            new_student.session = session
            new_student.save()
            form.save_m2m()

            messages.success(request, '%s added successful to the Session: %s' % (new_student.__str__(), session.name))
            return redirect('teacher-all-students', session.id)

    context = {'form':form}
    return render(request, 'teacher/student/add-student.html', context)


@teacher_only
def edit_student(request, session_pk, student_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=student_pk)

    form = StudentForm(instance = student)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance = student)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Student saved successfuly')
            return redirect('teacher-all-students', session_pk)

    context = {'form':form,}
    return render(request, 'teacher/student/edit-student.html', context)


@teacher_only
def delete_student(request, session_pk, student_pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=student_pk)
    
    if request.method == 'POST':
        messages.success(request,'The Student %s was deleted successfuly' % student)
        Student.delete(student)
        return redirect('teacher-all-students', session_pk)

    context = {'student':student}
    return render(request, 'teacher/student/delete-student.html', context)


