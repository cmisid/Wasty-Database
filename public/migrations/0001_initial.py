# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-12-28 17:45
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import public.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('first_name', models.CharField(blank=True, max_length=64, verbose_name='First name')),
                ('img', models.ImageField(blank=True, null=True, upload_to='users')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('last_name', models.CharField(blank=True, max_length=64, verbose_name='Last name')),
                ('oauth_id', models.CharField(max_length=128, verbose_name='OAuth id')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('date_joined',),
                'verbose_name_plural': 'Users',
                'db_table': 't_users',
            },
            managers=[
                ('objects', public.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'db_table': 't_cities',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.City')),
            ],
            options={
                'verbose_name_plural': 'Districts',
                'db_table': 't_districts',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('img', models.ImageField(blank=True, null=True, upload_to='items')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Date published')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('pub_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('pub_date',),
                'verbose_name_plural': 'Items',
                'db_table': 't_items',
            },
        ),
    ]
