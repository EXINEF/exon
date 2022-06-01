from django.test import TestCase
from app.models import Teacher
from django.contrib.auth.models import User, Group

class TestTeacherActions(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='teacher')
        Group.objects.create(name='student')

    def test_teacher_login_with_no_teacher_account_error(self):
        user = User.objects.create_user(username='noteacher', password='noteacher')
        user.save()
        response = self.client.post("/teacher/login", {'username':'noteacher','password':'noteacher'})
        self.assertEqual(response.status_code, 302)
    
    def test_teacher_login_with_teacher_account_and_redirect(self):
        user = User.objects.create_user(username='teacher', password='teacher')
        user.save()
        teacher = Teacher.objects.create(user=user,first_name='Mario',last_name='Rossi')
        teacher.save()
        response = self.client.post("/teacher/login", {'username':'teacher','password':'teacher'},follow=True)
        self.assertEqual(response.status_code, 200)

    def test_teacher_login_with_teacher_account_and_redirect_and_subject(self):
        user = User.objects.create_user(username='teacher', password='teacher')
        user.save()
        teacher = Teacher.objects.create(user=user,first_name='Mario',last_name='Rossi')
        teacher.save()
        response = self.client.post("/teacher/login", {'username':'teacher','password':'teacher'},follow=True)
        self.assertEqual(response.status_code, 200)

    def test_teacher_login_with_teacher_account_and_redirect_and_subject_and_add_subject(self):
        user = User.objects.create_user(username='teacher', password='teacher')
        user.save()
        teacher = Teacher.objects.create(user=user,first_name='Mario',last_name='Rossi')
        teacher.save()
        response = self.client.post("/teacher/login", {'username':'teacher','password':'teacher'},follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/teacher/add-subject")
        self.assertEqual(response.status_code, 200)
    
    def test_teacher_login_with_teacher_account_and_redirect_and_subject_and_add_subject_and_post(self):
        user = User.objects.create_user(username='teacher', password='teacher')
        user.save()
        teacher = Teacher.objects.create(user=user,first_name='Mario',last_name='Rossi')
        teacher.save()
        response = self.client.post("/teacher/login", {'username':'teacher','password':'teacher'},follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/teacher/add-subject")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/teacher/add-subject", {'name':'Matematica'},follow=True)
        self.assertEqual(response.status_code, 200)

    def test_teacher_login_with_teacher_account_and_redirect_and_subject_and_add_subject_and_post_and_subject(self):
        user = User.objects.create_user(username='teacher', password='teacher')
        user.save()
        teacher = Teacher.objects.create(user=user,first_name='Mario',last_name='Rossi')
        teacher.save()
        response = self.client.post("/teacher/login", {'username':'teacher','password':'teacher'},follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/teacher/add-subject")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/teacher/add-subject", {'name':'Matematica'},follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/teacher/subject/0")
        self.assertEqual(response.status_code, 200)

    def test_empty_teacher_login(self):
        response = self.client.post("/teacher/login", {'username':'','password':''},follow=True)
        self.assertEqual(response.status_code, 200)

    