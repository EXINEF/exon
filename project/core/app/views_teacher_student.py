from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *


@teacher_only
def allStudents(request):   
    teacher = get_object_or_404(Teacher, user=request.user)
    students = Student.objects.filter(teacher=teacher)

    context = {'students':students}
    return render(request, 'teacher/student/all-students.html', context)


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


@teacher_only
def editStudent(request, pk):   
    teacher = get_object_or_404(Teacher, user=request.user)  
    student = get_object_or_404(Student, id=pk, teacher=teacher)

    form = StudentForm(instance = student)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance = student)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Student saved successfuly')
            return redirect('teacher-all-students')

    context = {'form':form,}
    return render(request, 'teacher/student/edit-student.html', context)


@teacher_only
def deleteStudent(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, id=pk, teacher=teacher)
    
    if request.method == 'POST':
        messages.success(request,'The Student %s was deleted successfuly' % student)
        Student.delete(student)
        return redirect('teacher-all-students')

    context = {'student':student}
    return render(request, 'teacher/student/delete-student.html', context)


