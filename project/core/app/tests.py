from django.test import TestCase
from .models import Teacher

# Create your tests here.
class ModelsTest(TestCase):
    def test_get_full_name_teacher(self):
        t = Teacher(first_name='Mario',last_name='Rossi')
        self.assertEquals('Rossi Mario',t.get_full_name())

    def test_simple(self):
        self.assertEquals(1,1)

