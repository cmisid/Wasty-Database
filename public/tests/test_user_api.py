from django.test import TestCase
from rest_framework import status
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
        response = client.post('/users/', payload, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the user was correctly created directly in the database
        user = User.objects.get(email=self.email)
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))

        # Check the user was correctly created by doing an HTTP query
        response = client.get('/users/').json()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['email'], self.email)
        self.assertFalse('password' in response[0])
