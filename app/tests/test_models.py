from django.test import TestCase
from app.models import Teacher

class TestModels(TestCase):

    def test_get_full_name_teacher(self):
        t = Teacher(first_name='Mario',last_name='Rossi')
        self.assertEquals('Rossi Mario',t.get_full_name())

    def test_get_full_name_teacher_with_empty_first_name(self):
        t = Teacher(first_name='',last_name='Rossi')
        self.assertEquals('Rossi',t.get_full_name())

    def test_get_full_name_teacher_with_empty_last_name(self):
        t = Teacher(first_name='Mario',last_name='')
        self.assertEquals('Mario',t.get_full_name())

    def test_get_full_name_teacher_with_empty_first_name_and_empty_last_name(self):
        t = Teacher(first_name='',last_name='')
        self.assertEquals('',t.get_full_name())

    
