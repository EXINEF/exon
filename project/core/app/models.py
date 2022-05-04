from django.db import models
from django.contrib.auth.models import User
from pytz import utc
from requests import session
from datetime import timedelta
import datetime
from django.db.models.functions import Now

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

    def getNumOfQuestion(self):
        return Question.objects.filter(subject=self).count()

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
    duration = models.IntegerField(null=True)
    weight_correct_answer = models.FloatField(null=True, default=3)
    weight_blank_answer = models.FloatField(null=True, default=0)
    weight_wrong_answer = models.FloatField(null=True, default=-1)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    start_datetime = models.DateTimeField(null=True)
    expiration_datetime = models.DateTimeField(null=True)
    
    def __str__(self):
        return '%s - %s - %s' % (self.teacher, self.subject.name, self.start_datetime)

    def getName(self):
        return '%s - %s' % (self.start_datetime, self.expiration_datetime)

    def getExamsNumber(self):
        return Exam.objects.filter(session=self).count()

    def getExams(self):
        return Exam.objects.filter(session=self)

    def getStartedExams(self, exams):
        counter = 0
        for exam in exams:
            if exam.is_started():
                counter+=1
        return counter
    
    def getFinishedExams(self, exams):
        counter = 0
        for exam in exams:
            if exam.is_finished():
                counter+=1
        return counter

    def getMaximumScore(self):
        return self.weight_correct_answer * self.number_of_questions

class ExamQuestion(models.Model):
    pass

class Exam(models.Model):
    token = models.CharField(max_length=16, null=True, unique=True)

    student = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    start_datetime = models.DateTimeField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    correct_num = models.IntegerField(null=True)
    blank_num = models.IntegerField(null=True, default=0)
    wrong_num = models.IntegerField(null=True, default=0)
    votation = models.FloatField(null=True, default=0)
    
    def __str__(self):
        return '%s - %s - %s' % (self.token, self.student.username, self.session.subject.name)

    def is_started(self):
        return self.start_datetime is not None
    
    def is_finished(self):
        return self.finish_datetime is not None

    def getExpirationTime(self):
        return self.start_datetime + timedelta(minutes=self.session.duration)
        
    def isExpired(self):
        return self.getExpirationTime()<datetime.datetime.now(datetime.timezone.utc)

    def getStudentMatricola(self):
        s = self.student.username.split('_')
        return s[1]

    def analyzeExam(self):
        if not self.is_finished:
            raise Exception('Exam must be finish to be analyzed')
        
        questions = ExamQuestion.objects.filter(exam=self)

        self.correct_num = 0
        self.blank_num = 0
        self.wrong_num = 0
        self.votation = 0

        for q in questions:
            if q.answer is None:
                self.blank_num+=1
            elif q.answer.is_correct:
                self.correct_num+=1
            else:
                self.wrong_num+=1
        
        self.votation = (self.correct_num*self.session.weight_correct_answer + self.blank_num*self.session.weight_blank_answer + self.wrong_num*self.session.weight_wrong_answer) /  questions.count() * self.session.weight_correct_answer
            

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s %s' % (self.exam, self.question, self.answer)

    def is_answered(self):
        return self.answer is not None

class Student(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    matricola = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s - %s' % (self.matricola, self.full_name())

    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)