from django.test import TestCase

from public.models import User


class UserTestCase(TestCase):

    email = 'alice@carol.com'
    first_name = 'Alice'
    last_name = 'Kinsley'
    oauth_id = '123'
    password = 'wonderland'

    def setUp(self):
        user = User(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            oauth_id=self.oauth_id
        )
        user.set_password(self.password)
        user.save()

    def test_password(self):
        """Check that the user's password has been hashed."""
        user = User.objects.get(email=self.email)
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
