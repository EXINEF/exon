from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.full_name(), self.user.username)

    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)


class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.name, self.teacher.full_name())

class Question(models.Model):
    text = models.TextField(null=True)
    difficulty = models.IntegerField(null=True)
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.teacher.full_name(), self.text)

class Answer(models.Model):
    text = models.TextField(null=True)
    is_correct = models.BooleanField(default=False, null=True)
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if(self.text is None):
            return 'NONE'
        return self.question.__str__() + ' --- ' +self.text  +' --- ' +  str(self.is_correct)

class Session(models.Model):
    number_of_questions = models.IntegerField(null=True)
    number_of_exams = models.IntegerField(null=True)
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    start_datetime = models.DateTimeField(null=True)
    expiration_datetime = models.DateTimeField(null=True)
    
    def __str__(self):
        return '%s - %s - %s' % (self.teacher, self.subject.name, self.start_datetime)

    def getName(self):
        return '%s - %s' % (self.start_datetime, self.expiration_datetime)

class Exam(models.Model):
    token = models.CharField(max_length=16, null=True, unique=True)
    matricola = models.CharField(max_length=16, null=True)
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    start_datetime = models.DateTimeField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    
    def __str__(self):
        return '%s - %s - %s' % (self.token, self.matricola, self.session.subject.name)

    def is_started(self):
        return self.start_datetime is not None
    
    def is_finished(self):
        return self.finish_datetime is not None

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s %s' % (self.exam, self.question, self.answer)