import random
import string
from .models import Exam, ExamQuestion, Question
from django.contrib.auth.models import User

def random_token_generator(str_size):
    allowed_chars = string.ascii_letters
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

# ALL THE QUESTIONS IN AN EXAM ARE DIFFERENT
def generateNQuestionsForExam(exam, n):
    lst = []
    for i in range(n):
        question = Question.objects.order_by('?')[0]
        exam_question = ExamQuestion(exam=exam, question=question)
        
        while(question.text in lst):
            question = Question.objects.order_by('?')[0]
            exam_question = ExamQuestion(exam=exam, question=question)
        
        exam_question.save()
        lst.append(question.text)

def generateUserExamQuestionsForStudent(session, student):
    TOKEN_SIZE = 10
    token = random_token_generator(TOKEN_SIZE)
    new_username = 'E' + str(session.id)+'_'+student.matricola
    new_student_user = User(username = new_username, password=token)
    new_student_user.save()

    exam = Exam(token=token, student=new_student_user, session=session)
    exam.save()
    generateNQuestionsForExam(exam, session.number_of_questions)


def getAnswerValue(value):
    if value is None:
        return 0
    return 1

