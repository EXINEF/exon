from statistics import mode
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
	first_name = models.CharField(max_length=255, blank=True, null=True)
	last_name = models.CharField(max_length=255, blank=True, null=True)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	creation_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	
	def __str__(self):
		return '%s ( %s %s )' % (self.user.username, self.first_name, self.last_name)


class Subject(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, blank=True, null=True)
	
	creation_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	
	def __str__(self):
		return self.name


class Answer(models.Model):
	text = models.TextField(blank=True, null=True)
	is_correct = models.BooleanField(default=False, blank=True, null=True)
	creation_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	
	def __str__(self):
		return str(self.is_correct) + ' - ' + self.text


class Question(models.Model):
	text = models.TextField(blank=True, null=True)
	difficulty = models.IntegerField(blank=True, null=True)
	subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, blank=True, null=True)
	
	answers = models.ManyToManyField(Answer, blank=True)
	
	creation_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	
	def __str__(self):
		return self.text
