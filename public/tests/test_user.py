from django.test import TestCase

from public.models import User


class UserTestCase(TestCase):

    email = 'alice@carol.com'
    password = 'wonderland'

    def setUp(self):
        user = User(email=self.email)
        user.set_password(self.password)
        user.save()

    def test_password(self):
        """Check that the user's password has been hashed."""
        user = User.objects.get(email=self.email)
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
