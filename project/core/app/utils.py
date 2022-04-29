import random
import string
from .models import Exam, ExamQuestion, Question
 
def random_token_generator(str_size):
    allowed_chars = string.ascii_letters
    return ''.join(random.choice(allowed_chars) for x in range(str_size))
 
def generateNExamsForSession(session):
    TOKEN_SIZE = 10
    for i in range(session.number_of_exams):
        token = random_token_generator(TOKEN_SIZE)
        while(Exam.objects.filter(token=token).exists()):
            token = random_token_generator(TOKEN_SIZE)
        exam = Exam(token=token, matricola='TODO',session=session)
        exam.save()
        generateNQuestionsForExam(exam, session.number_of_questions)

def generateNStudentsAccountForSession(session):
    # TODO generate accounts username with matricola code and password with token
    return

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
