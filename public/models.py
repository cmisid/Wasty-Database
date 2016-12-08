from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

import os


class User(AbstractUser):

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        ordering = ('date_joined',)

    def __str__(self):
        return self.get_full_name()


class Item(models.Model):

    class Meta:
        db_table = 'items'
        verbose_name_plural = 'Items'
        ordering = ('pub_date',)

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    img = models.ImageField(upload_to='img', null=True)
    img_url = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField('Date published', auto_now_add=True)
    pub_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def render_image(self):
        return '<img src="{}" width="100px"/>'.format(os.path.join('localhost:8000/static/img', self.img_url))
    render_image.allow_tags = True

    def little_description(self):
        return self.description[:100]

    def __str__(self):
        return self.name
