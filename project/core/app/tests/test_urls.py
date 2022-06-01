from django.test import TestCase

class TestUrls(TestCase):

    def test_index_access(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_teacher_login(self):
        response = self.client.get("/teacher/login")
        self.assertEqual(response.status_code, 200)
    
    def test_student_login(self):
        response = self.client.get("/student/login")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access(self):
        response = self.client.get("/teacher/dashboard")
        self.assertEqual(response.status_code, 302)

    def test_add_subject(self):
        response = self.client.get("/teacher/add-subject")
        self.assertEqual(response.status_code, 302)
    
    def test_subject_access_with_subject(self):
        response = self.client.get("/teacher/subject/0")
        self.assertEqual(response.status_code, 302)

    def test_start_exam(self):
        response = self.client.get("/student/start-exam")
        self.assertEqual(response.status_code, 302)

    def test_exam_access_with_exam(self):
        response = self.client.get("/student/exam/0")
        self.assertEqual(response.status_code, 302)
    





        
    