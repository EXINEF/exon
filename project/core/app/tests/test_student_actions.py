from django.test import TestCase
from app.models import Teacher, Exam
from django.contrib.auth.models import User, Group

class TestStudentActions(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='teacher')
        Group.objects.create(name='student')

    def test_student_login_with_student_account_and_redirect(self):
        user = User.objects.create_user(username='student', password='student')
        user.save()
        group = Group.objects.get(name='student')
        user.groups.add(group)
        user.save()

        response = self.client.post('/student/login', {'username': 'student', 'password': 'student'})
        self.assertEqual(response.status_code, 200)

    


