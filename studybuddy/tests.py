from django.test import TestCase
from .models import User

# Create your tests here.
class ModelTesting(TestCase):
    def test_model(self):
        self.user = User.objects.create(username='jacqueline-chao', password='123')
        self.assertTrue(isinstance(self.user, User))