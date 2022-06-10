from datetime import timedelta, datetime, timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.get_full_name(), self.user.username)
    
    def get_full_name(self):
        if self.last_name == '':
            return self.first_name
        if self.first_name == '':
            return self.last_name
        return '%s %s' % (self.last_name, self.first_name)


class SubjectStatistics(models.Model):
    class Meta:
        verbose_name_plural = "Subject Statistics"

    total_sessions = models.IntegerField(blank=True, null=True)
    not_started_sessions = models.IntegerField(blank=True, null=True)
    started_sessions = models.IntegerField(blank=True, null=True)
    finished_sessions = models.IntegerField(blank=True, null=True)
      
    total_exams = models.IntegerField(blank=True, null=True)
    started_exams = models.IntegerField(blank=True, null=True)
    finished_exams = models.IntegerField(blank=True, null=True)
    average_votation_exams_10 = models.IntegerField(blank=True, null=True) 
    average_votation_exams_30 = models.IntegerField(blank=True, null=True)
    
    total_questions = models.IntegerField(blank=True, null=True)
    correct_questions = models.IntegerField(blank=True, null=True)
    blank_questions = models.IntegerField(blank=True, null=True)
    wrong_questions = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if not Subject.objects.filter(statistics=self).exists():
            return 'Statistics Not Associated'
        return 'Statistics of %s' % (Subject.objects.get(statistics=self))

    def reset_all(self):
        self.total_sessions = 0
        self.not_started_sessions = 0
        self.started_sessions = 0
        self.finished_sessions = 0
        
        self.total_exams = 0
        self.started_exams = 0
        self.finished_exams = 0
        self.average_votation_exams_10 = 0
        self.average_votation_exams_30 = 0
        
        self.total_questions = 0
        self.correct_questions = 0
        self.blank_questions = 0
        self.wrong_questions = 0
        

class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    statistics = models.OneToOneField(SubjectStatistics, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.name, self.teacher.get_full_name())
    
    def get_display_description(self):
        if self.description is None or self.description == '':
            return 'No description available.'
        return self.description[:30] + '...'

    def get_number_of_questions(self):
        return Question.objects.filter(subject=self).count()
    
    def get_number_of_exams(self):
        number_of_exams = 0
        sessions = Session.objects.filter(subject=self)
        for session in sessions:
            number_of_exams += Exam.objects.filter(session=session)
        return number_of_exams

    def get_numbers_of_sessions(self):
        not_started = 0
        started = 0
        finished = 0

        sessions = Session.objects.filter(subject=self)
        for session in sessions:
            if not session.is_started:
                not_started += 1
            elif session.is_started and not session.is_finished:
                started += 1
            else:
                finished += 1
        return not_started,started,finished

    def calculate_statistics(self):
        self.statistics.reset_all()
        votation = 0
        sessions = Session.objects.filter(subject=self)
        self.statistics.total_sessions = sessions.count()
        
        for session in sessions:
            if session.get_status() == 'STARTED':
                self.statistics.started_sessions += 1
            elif session.get_status() == 'FINISHED':
                self.statistics.finished_sessions += 1	
            else:
                self.statistics.not_started_sessions += 1

            exams = Exam.objects.filter(session=session)	
            self.statistics.total_exams += exams.count()

            for exam in exams:
                if exam.is_started():
                    self.statistics.started_exams += 1
                
                if exam.is_finished():
                    self.statistics.finished_exams += 1
                    self.statistics.correct_questions += exam.correct_num
                    self.statistics.blank_questions += exam.blank_num
                    self.statistics.wrong_questions += exam.wrong_num
                    votation += exam.get_votation_out_of_10()
                        
        self.statistics.total_questions = self.statistics.correct_questions+self.statistics.blank_questions+self.statistics.wrong_questions
        if self.statistics.finished_exams > 0:
            self.statistics.average_votation_exams_10 = votation/self.statistics.finished_exams
            self.statistics.average_votation_exams_30 = self.statistics.average_votation_exams_10*3
        else:
            self.statistics.average_votation_exams_10 = 0
            self.statistics.average_votation_exams_30 = 0
        self.statistics.save()

class Question(models.Model):

    DIFFICULTY = (
        ('VERY EASY', 'VERY EASY'),
        ('EASY', 'EASY'),
        ('NORMAL', 'NORMAL'),
        ('DIFFICULT', 'DIFFICULT'),
        ('VERY DIFFICULT', 'VERY DIFFICULT'),
    )

    text = models.TextField(null=True)
    difficulty = models.CharField(max_length=100, default='NORMAL', blank=True, null=True, choices=DIFFICULTY)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.teacher.get_full_name(), self.text)

    def get_type(self):
        if Answer.objects.filter(question=self, is_correct=True).count()==1:
            return 'SINGLE CHOICE'
        return 'MULTIPLE CHOICE'
        
    def get_statistics(self):
        questions = ExamQuestion.objects.filter(question=self)
        correct = 0
        blank = 0
        for question in questions:
            status = question.get_status()
            if status=='CORRECT':
                correct += 1
            elif status=='BLANK':
                blank +=1
        return questions.count(),correct, blank, (questions.count()-correct-blank) 


class Answer(models.Model):
    text = models.TextField(null=True)
    is_correct = models.BooleanField(default=False, null=True)
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        if (self.text is None):
            return 'NONE'
        return self.question.__str__() + ' --- ' + self.text + ' --- ' + str(self.is_correct)

class Session(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    is_locked = models.BooleanField(default=True, null=True)
    is_started = models.BooleanField(default=False, null=True)
    is_finished = models.BooleanField(default=False, null=True)

    number_of_questions = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    weight_correct_answer = models.FloatField(blank=True, null=True, default=3)
    weight_blank_answer = models.FloatField(blank=True, null=True, default=0)
    weight_wrong_answer = models.FloatField(blank=True, null=True, default=-1)
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)

    start_datetime = models.DateTimeField(null=True)
    expiration_datetime = models.DateTimeField(null=True)
    
    def __str__(self):
        return '%s - %s - %s' % (self.teacher, self.subject.name, self.start_datetime)
    
    def get_display_description(self):
        if self.description is None or self.description == '':
            return 'No description available.'
        return self.description[:30] + '...'
    
    def is_open(self):
        return self.start_datetime < datetime.now() and self.expiration_datetime > datetime.now()
    
    def is_not_started(self):
        return not self.is_open() and self.start_datetime > datetime.now(timezone.utc)
    
    def is_configurated(self):
        return self.number_of_questions and self.duration is not None

    def get_status(self):
        if not self.is_configurated():
            return 'MISSING CONFIGURATION'
        if not self.is_started:
            return 'READY'
        if not self.is_finished:
            return 'STARTED'
        else:
            return 'FINISHED'
    
    def get_students_registered(self):
        return Student.objects.filter(session=self).count()
    
    def get_exams(self):
        return Exam.objects.filter(session=self)
    
    def get_started_exams(self, exams):
        counter = 0
        for exam in exams:
            if exam.is_started():
                counter += 1
        return counter
    
    def get_finished_exams(self, exams):
        counter = 0
        for exam in exams:
            if exam.is_finished():
                counter += 1
        return counter
    
    def get_max_votation(self):
        return self.weight_correct_answer * self.number_of_questions

    def set_finished(self):
        self.is_locked = True
        self.is_finished = True
        exams = self.get_exams()
        for exam in exams:
            if not exam.is_finished():
                exam.set_finished()
                exam.save()

    def allowed_status(self, status_list):
        session_status = self.get_status()
        for status in status_list:
            if session_status == status:
                return True
        return False

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
        return '%s - %s' % (self.token, self.session.subject.name)

    def is_started(self):
        return self.start_datetime is not None
    
    def is_finished(self):
        return self.finish_datetime is not None

    def set_started(self):
        self.start_datetime = datetime.now()

    def set_finished(self):
        self.finish_datetime = datetime.now()
        self.analyze_and_correct_exam()

    def get_start_datetime(self):
        return self.start_datetime.strftime('%d-%m-%Y %H:%M')

    def get_finish_datetime(self):
        return self.finish_datetime.strftime('%d-%m-%Y %H:%M')

    def get_start_infos(self):
        if self.start_datetime is None:
            return 'Not started yet.'
        return 'Started at %s' % self.get_start_datetime()
    
    def get_finish_infos(self):
        if self.finish_datetime is None:
            return 'Not finished yet.'
        return 'Finished at %s' % self.get_finish_datetime()
    
    def get_expiration_time(self):
        print(self.session.duration)
        return self.start_datetime + timedelta(minutes=self.session.duration)
    
    def is_expired(self):
        print('START TIME\n' +str(self.start_datetime))
        print('EXPIRATION TIME\n' +str(self.get_expiration_time()))
        print('\nCURRENT DATETIME\n' +str(datetime.now()))
        print(type(self.get_expiration_time()))
        print(type(datetime.now()))
        return self.get_expiration_time() < datetime.now()
    
    def get_votation_out_of_10(self):
        return int(self.votation / self.session.get_max_votation() * 10)

    def get_votation_out_of_30(self):
        return int(self.votation / self.session.get_max_votation() * 30)

    def analyze_and_correct_exam(self):
        if not self.is_finished:
            raise Exception('Exam must be finish to be analyzed')
        
        questions = ExamQuestion.objects.filter(exam=self)
        
        self.correct_num = 0
        self.blank_num = 0
        self.wrong_num = 0
        self.votation = 0
        
        for q in questions:
            status = q.get_status()

            if status == 'CORRECT':
                self.correct_num += 1
            elif status == 'BLANK':
                self.blank_num += 1
            else:
                self.wrong_num += 1

        self.votation = self.correct_num * self.session.weight_correct_answer + self.blank_num * self.session.weight_blank_answer + self.wrong_num * self.session.weight_wrong_answer
        
        if self.votation<0:
            self.votation = 0
        
        self.votation = format(self.votation, ".2f")
        self.save()

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
        
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.exam, self.question)
    
    def is_answered(self):
        return ExamAnswer.objects.filter(exam_question = self).count()!=0

    def delete_all_answers(self):
        ExamAnswer.objects.filter(exam_question=self).delete()

    def get_status(self):
        if not self.is_answered():
            return 'BLANK'
        if self.is_correct():
            return 'CORRECT'
        return 'WRONG'

    def is_correct(self):
        answers = ExamAnswer.objects.filter(exam_question=self)
        for answer in answers:
            if not answer.answer.is_correct:
                return False
        return True

    def has_this_answer(self, pk):
        exam_answers = ExamAnswer.objects.filter(exam_question=self)
        for a in exam_answers:
            if a.answer.pk == pk:
                return True
        return False
    
    def get_status_of_answer(self, pk):
        exam_answers = ExamAnswer.objects.filter(exam_question=self)
        for a in exam_answers:
            if a.answer.pk == pk:
                if a.answer.is_correct:
                    return 'CORRECT'
                else:
                    return 'WRONG'
        return 'BLANK'

    def get_all_possibles_answers(self):
        return Answer.objects.filter(question=self.question)

class ExamAnswer(models.Model):
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)\

    creation_datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.exam_question, self.answer)

class Student(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=50, null=True)
    matricola = models.CharField(max_length=50, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.matricola, self.get_full_name())
    
    def get_full_name(self):
        return '%s %s' % (self.last_name, self.first_name)

class Access(models.Model):
    class Meta:
        verbose_name_plural = "Accesses"

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    ip = models.CharField(max_length=255, null=True)
    creation_datetime = models.DateTimeField(auto_now_add=True, null=True) 

    def get_number_of_access_tokens(self):
        return Access.objects.filter(exam=self.exam).count()

    def get_creation_datetime(self):
        return self.creation_datetime.strftime('%d-%m-%Y %H:%M')


def get_matricola_from_user(self):
    students = Student.objects.filter(email=self.email)
    if students.exists():
        return students[0].matricola
    else:
        'MATRICOLA NOT FOUND'

# Add a custom method to the Default Django Class User    
User.add_to_class('get_matricola_from_user', get_matricola_from_user)
