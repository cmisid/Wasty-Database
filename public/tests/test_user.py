from django.test import TestCase

from public.models import User


class UserTestCase(TestCase):

    username = 'Alice'
    password = 'wonderland'

    def setUp(self):
        user = User(username=self.username)
        user.set_password(self.password)
        user.save()

    def test_password(self):
        """Check that the user's password has been hashed."""
        user = User.objects.get(username=self.username)
        self.assertNotEqual(user.password, self.password)
