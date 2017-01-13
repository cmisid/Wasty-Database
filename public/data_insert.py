import json
import psycopg2
import requests

from public.models import District, City, CenterOfInterest, User
from django.db import connection
from django.contrib.gis.geos import Point


def read_json(fichier):
	json_data = open(fichier)
	data = json.load(json_data)
	json_data.close()
	return data


def insert_district(data, city):
    for i in range(0, 60):
        popo='POLYGON (({}))'.format(', '.join((
                '{} {}'.format(coord[0], coord[1])
                for coord in data[i]['Geo Shape']
            )))
        new_district = District(district_name=data[i]['Libelle des grands quartiers'],
            density=data[i]['densite'],
            polygon=popo,
            city_id=city
            )
        district = new_district.save()


def insert_centerofinterest(data):
    for i in range(0, 21):
        new_center = CenterOfInterest(name_center_of_interest=data[i]['center']).save()


def insert_category(data):
    for i in range(0, 9):
        print(data[i])
        new_center = Category(category_name=data[i]['category']).save()
