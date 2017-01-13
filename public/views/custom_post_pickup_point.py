# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.gis.geos import Point

from public.models import PickUpPoint, Address, City, District
from public import modify_address


@csrf_exempt
def city_exist(a_city):
    """recherche de la city ajoute dans la bd"""
    city_name = a_city
    if not City.objects.filter(city_name=city_name).exists():
        city = City(city_name=city_name).save()
        city = City.objects.get(city_name=city_name)
    else:
        city = City.objects.get(city_name=city_name)
    return(city.id)


@csrf_exempt
def address_exist(payload):
    """cherche si l'adresse existe dans la bd si oui renvoi l'id sinon la creee"""
    loc = payload.get('geo_shape')
    a_city = None
    location = Point((loc[1], loc[0]))
    if modify_address.geocoder_reverse(location) != 'ERROR':
        (a_number, a_name, a_cp, a_city) = modify_address.geocoder_reverse(location)
        if not Address.objects.filter(location=location).exists():
            new_address=Address(
                street_number=a_number,
                street_name=a_name,
                postal_code=a_cp,
                address_city_id=city_exist(a_city),
                location=location
            )
            address = new_address.save()
            address = Address.objects.get(location=location)
            return(address.id)
        else:
            address = Address.objects.get(location=location)
            return(address.id)
    else:
        return(None)

@csrf_exempt
def recovery_type_exists(payload):
    """recherche le type de pick up point"""
    recovery_type=payload.get('categorie')
    if recovery_type is None:
        return None
    else:
        recovery = {
            'emballage': '1',
            'verre': '2',
            'textile': '3'
            }
        return recovery[recovery_type]


@csrf_exempt
def post_pickup_point(request):
    """insert les nouveaux points de collect lorsque l'adress est reconnu par geolocalisation"""
    try:
        data = json.loads(request.body.decode())
        for i in range(0, len(data)):
            payload = data[i]
            print(payload.get('id_poi'))
            print(i)
            if address_exist(payload) is not None:
                print("rentre 1")
                pickuppoint = PickUpPoint(
                    pickup_point_address_id=address_exist(payload),
                    recovery_type=recovery_type_exists(payload)
                    )
                if not PickUpPoint.objects.filter(pickup_point_address_id=address_exist(payload)).exists():
                    print("rentre 2")
                    pickuppoint.save()
        return HttpResponse(status=201)

    except Exception as err:
        print(err)
        return HttpResponse(status=400)

