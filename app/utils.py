import random
import string
import os
import mimetypes
import yaml

from .models import Exam, ExamQuestion, Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.core.files import File
from core.settings import TOKEN_SIZE


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
    token = random_token_generator(TOKEN_SIZE)
    while Exam.objects.filter(token=token).exists():
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


def get_converted_questions_and_answers_to_yaml(questions):
    data = ''
    for question in questions:
        answers = Answer.objects.filter(question=question)
        data += '- question: '+question.text+'\n'
        data += '  difficulty: '+question.difficulty+'\n\n'
        counter = 0

        for answer in answers:
            data += '  answer'+str(counter)+': '+answer.text+'\n'
            data += '  is_correct'+str(counter)+': '+str(answer.is_correct)+'\n\n'
            counter += 1
        
        data += '\n'

    return data

def save_questions_and_answers_from_yaml(file, teacher, subject):
    file_data = file.read().decode('utf-8')
    yaml_questions = yaml.safe_load(file_data)
    
    for question in yaml_questions:
        new_question = Question(text=question['question'], difficulty=question['difficulty'], subject=subject, teacher=teacher)
        new_question.save()
        counter = 0

        for n in range(4):
            new_answer = Answer(text=question['answer'+str(counter)], is_correct=question['is_correct'+str(counter)], question=new_question)
            new_answer.save()
            counter += 1


def get_response_download_questions_and_answers_file(questions, teacher, subject):
    yaml_data = get_converted_questions_and_answers_to_yaml(questions)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = teacher.user.username + '_' + str(subject.id) + '_questions_backup.yaml'
    filepath = BASE_DIR + filename

    stream = open(filepath, 'w')
    file = File(stream)
    file.write(yaml_data)
    file.close()
    stream.close()
    
    stream = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(stream, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename    
    return response