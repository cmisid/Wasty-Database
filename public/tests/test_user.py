from django.test import TestCase
from rest_framework.test import APIRequestFactory

from public.models import User


class UserTestCase(TestCase):

    username = 'Alice'
    password = 'wonderland'

    def setUp(self):
        factory = APIRequestFactory()
        request = factory.post('/users/', {
            'username': self.username,
            'password': self.password
        })

    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_password(self):
        """Check that the user's password has been hashed."""
        user = User.objects.get(username=self.username)
        self.assertNotEqual(user.password, self.password)
