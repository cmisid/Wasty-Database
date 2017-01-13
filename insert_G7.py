import json
import psycopg2
import requests

from public.models import District, City, CenterOfInterest, User
from django.db import connection
from django.contrib.gis.geos import Point
from public.views import custom_post_user
from public import data_insert


def insert_user(data):
    print("coucou")
    for i in range(0, len(data)):
        r = requests.post('http://127.0.0.1:8000/post_user', json=data[i])
        custom_post_user.post_user(data[i])


if __name__ == '__main__':
    if not User.objects.filter(id=1).exists():
        print("coucou")
        insert_user('./Data/users.json')
