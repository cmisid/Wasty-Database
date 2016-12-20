from django.test import TestCase
from rest_framework.test import APIClient

from public.models import User


class APIUserTestCase(TestCase):

    email = 'alice@carol.com'
    password = 'wonderland'

    def test_register(self):
        """Check that the user can register through the API."""
        client = APIClient()
        payload = {
            'email': self.email,
            'password': self.password
        }
        client.post('/users/', payload, format='json')

        user = User.objects.get(email=self.email)
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
