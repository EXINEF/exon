from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from io import StringIO

import csv
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
def load_file_students(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    session = get_object_or_404(Session, id=pk, teacher=teacher)

    if request.method == 'POST':
        
        upload_file = request.FILES['file']
        file_name = upload_file._get_name().split('.')

        if len(file_name)!=2 or file_name[1]!='csv':
            messages.error(request, 'ERROR: the file must be a .csv like this: file.csv')
            return redirect('teacher-all-students', session.pk)
        file = upload_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')

        for row in csv_data:
            if len(row) != 4:
                messages.error(request, 'ERROR: the file must have 4 string for each row, like this: matricola_number, surname, name, email ')
                return redirect('teacher-all-students', session.pk)

            if Student.objects.filter(session=session, matricola=row[0]).exists(): 
                messages.error(request, 'ERROR: a student with this matricola( %s ) already exist in this session.' % (row[0].replace(' ', '')))
            else:    
                Student.objects.create(
                    first_name=row[2].replace(' ', ''),
                    last_name=row[1].replace(' ', ''),
                    email = row[3].replace(' ', ''),
                    matricola = row[0].replace(' ', ''),
                    session=session
                )
        messages.success(request, 'Your students were loaded successfuly for session: %s' % (session.name))
        return redirect('teacher-all-students', session.pk)
        
    context = {'session':session}
    return render(request, 'teacher/student/load-file-students.html', context)


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


