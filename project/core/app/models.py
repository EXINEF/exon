from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
	first_name = models.CharField(max_length=255, null=True)
	last_name = models.CharField(max_length=255, null=True)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return '%s ( %s %s )' % (self.user.username, self.first_name, self.last_name)


class Subject(models.Model):
	name = models.CharField(max_length=50, null=True)
	description = models.TextField(blank=True, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	
	creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return self.name

class Question(models.Model):
	text = models.TextField(null=True)
	difficulty = models.IntegerField(null=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	
	creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return self.text

class Answer(models.Model):
	text = models.TextField(null=True)
	is_correct = models.BooleanField(default=False, null=True)
	creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	
	def __str__(self):
		return str(self.is_correct) + ' - ' + self.text



