import random
import string
from .models import Exam, ExamQuestion, Question, Student
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

def select_random_question_poll_from_subject(subject, number_of_questions):
    questions = []

    for i in range(number_of_questions):
        question = Question.objects.filter(subject=subject).order_by('?')[0]

        while question in questions:
            question = Question.objects.order_by('?')[0]

        questions.append(question)
    
    return questions


def generate_questions_for_exam(exam, question_poll):
    random.shuffle(question_poll)
    for question in question_poll:
        exam_question = ExamQuestion(exam=exam, question=question)
        exam_question.save()


def random_token_generator(str_size):
    allowed_chars = string.ascii_uppercase
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


def generate_user_and_exam_for_student(session, student, questions_poll):
    TOKEN_SIZE = 10
    token = random_token_generator(TOKEN_SIZE)
    new_student_user = User.objects.create_user(username=token, password=token, email=student.email, first_name=student.first_name, last_name=student.last_name)
    
    teacher_group = Group.objects.get(name='student')
    teacher_group.user_set.add(new_student_user)
    
    exam = Exam(token=token, student=new_student_user, session=session)
    exam.save()
    generate_questions_for_exam(exam, questions_poll)


def getAnswerValue(value):
    if value is None:
        return 0
    return 1

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_token_by_email_for_exam(session, exam):
    mail_object = 'TOKEN EXAM SESSION: '+session.name
    mail_body = 'Hello, this is the token for entering your exam: '+ exam.token

    email = EmailMessage(mail_object, mail_body, to=[exam.student.email])
    email.send()

def get_answer_value(value):
    if value is None:
        return False
    return True

