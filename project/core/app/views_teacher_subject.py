from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .decorators import *
from .forms import *
from .filters import QuestionFilter

@teacher_only
def subject_page(request, pk):
	teacher = get_object_or_404(Teacher, user=request.user)
	subject = get_object_or_404(Subject, id=pk, teacher=teacher)
	num_questions = Question.objects.filter(subject=subject).count()
	sessions = Session.objects.filter(subject=subject, teacher=teacher)
	
	context = {'subject': subject, 'num_questions': num_questions, 'sessions': sessions}
	return render(request, 'teacher/subject/subject.html', context)


@teacher_only
def load_questions_file(request, pk):
	context = {}
	return render(request, 'teacher/subject/load-questions-file.html', context)


@teacher_only
def add_subject(request):
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
	
	context = {'form': form}
	return render(request, 'teacher/subject/add-subject.html', context)


@teacher_only
def delete_subject(request, pk):
	teacher = get_object_or_404(Teacher, user=request.user)
	subject = get_object_or_404(Subject, id=pk, teacher=teacher)
	
	if request.method == 'POST':
		messages.success(request, 'The Subject %s was deleted successfuly' % subject.name)
		Subject.delete(subject)
		return redirect('teacher-dashboard')
	
	context = {'subject': subject}
	return render(request, 'teacher/subject/delete-subject.html', context)


@teacher_only
def edit_subject(request, pk):
	teacher = get_object_or_404(Teacher, user=request.user)
	subject = get_object_or_404(Subject, id=pk, teacher=teacher)
	
	form = SubjectForm(instance=subject)
	
	if request.method == 'POST':
		form = SubjectForm(request.POST, instance=subject)
		
		if form.is_valid():
			form.save()
			messages.success(request, 'Subject saved successfuly')
			return redirect('teacher-dashboard')
	
	context = {'form': form, }
	return render(request, 'teacher/subject/edit-subject.html', context)


@teacher_only
def edit_questions(request, pk, page, results):
	teacher = get_object_or_404(Teacher, user=request.user)
	subject = get_object_or_404(Subject, id=pk, teacher=teacher)
	total_questions = Question.objects.filter(subject=subject).count()
	questions = Question.objects.filter(subject=subject)[page * results:(page +1)*results]

	myFilter = QuestionFilter(request.GET, queryset=questions)
	questions = myFilter.qs

	if page <= 0:
		previous = 0
		next = 1
	else:
		previous = page - 1
		next = page + 1
	context = {'subject': subject, 'questions': questions, 'total_questions':total_questions, 'myFilter':myFilter, 'page':page, 'results':results, 'previous':previous, 'next':next}
	return render(request, 'teacher/subject/edit-questions.html', context)
