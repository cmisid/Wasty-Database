from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        ordering = ('join_date',)

    birth_date = models.DateField(verbose_name='Birthdate', null=True)
    join_date = models.DateField(verbose_name='Joined', auto_now_add=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()


class Item(models.Model):

    class Meta:
        db_table = 'items'
        verbose_name_plural = 'Items'
        ordering = ('pub_date',)

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    img_url = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField('Date published', auto_now_add=True)
    pub_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def render_image(self):
        return '<img src="{}"/>'.format(self.img_url)

    def __str__(self):
        return self.name
