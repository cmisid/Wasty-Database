import json
#import requests

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.gis.geos import Point

from public.models import User, Address, City, CenterOfInterest, InterestFor, District
from public import modify_address
from public import data_insert as di

@csrf_exempt
def city_exist(payload):
    """recherche de la city ajoute dans la bd"""
    city_name = payload.get('city_name')
    if not City.objects.filter(city_name=city_name).exists():
        city = City(city_name=city_name).save()
        city = City.objects.get(city_name=city_name)
    else:
        city = City.objects.get(city_name=city_name)
    return(city.id)


@csrf_exempt
def district_exist(payload):
    """recherche le quartier"""
    name_district = payload.get('districts')
    if not District.objects.filter(id=1).exists():
        city = City(city_name='Toulouse').save()
        city = City.objects.get(city_name='Toulouse')
        di.insert_district(di.read_json('./Data/district.json'), city.id)
    elif name_district is None:
        return (District.objects.get(district_name='NULL').id)
    else:
        return(District.objects.get(district_name=name_district).id)


@csrf_exempt
def address_exist(payload):
    """cherche si l'adresse existe dans la bd si oui renvoi l'id sinon la creee"""
    a_number = payload.get('street_number', None)
    a_name = payload.get('street_name', None)
    a_cp = payload.get('postcode', None)
    if a_number == None or a_name == None or a_cp == None:
        print("sans adresse")
        return(None)
    a_complement = payload.get('complement', None)
    a_district = district_exist(payload)
    a_ville = city_exist(payload)
    #print(a_number, a_name, a_cp, a_ville)
    #print(modify_address.geocoder(('2','chemin des sauges','31400','TOULOUSE')))

    if not Address.objects.filter(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement).exists():
            new_address = Address(
                street_number=a_number,
                street_name=a_name,
                postal_code=a_cp,
                address_city_id=a_ville,
                district_id=a_district,
                location=Point(modify_address.geocoder((a_number, a_name, a_cp, a_ville)))
            )
            address = new_address.save()
            address = Address.objects.get(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement)
    else:
        address = Address.objects.get(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement)

    return(address.id)


@csrf_exempt
def test_email(payload):
    """verifie email unique"""
    email = payload.get('email')
    if not User.objects.filter(email=email).exists():
        return email
    else:
        return HttpResponse(status=400)


@csrf_exempt
def CenterOfInterest_exist(CenterInterest):
    """verifie centre interet existe"""
    if not CenterOfInterest.objects.filter(id=1).exists():
        di.insert_centerofinterest(di.read_json('./Data/centerInterest.json'))
        return(CenterOfInterest.objects.get(name_center_of_interest=CenterInterest).id)
    else:
        print(CenterOfInterest.objects.get(name_center_of_interest=CenterInterest))
        return(CenterOfInterest.objects.get(name_center_of_interest=CenterInterest).id)

@csrf_exempt
def gender_exist(payload):
    name_gender = payload.get('gender')
    if name_gender is None:
        return (None)
    else:
        g = {'Homme': 'M', 'Femme': 'F'}
        return g[name_gender]

@csrf_exempt
def csp_exist(payload):
    """renvoi la csp du user"""
    name_csp = payload.get('social_professional_category')
    if name_csp is None:
        return (None)
    else:
        csp = {'artisans, commercants, chefs entreprise': '1',
            'cadres et professions intellectuelles superieures': '2',
            'professions intermediaires': '3',
            'employes': '4',
            'ouvriers': '5',
            'retraites': '6',
            'chomeurs': '7',
            'etudiants': '8',
            'autres': '9'
            }
        return csp[name_csp]

@csrf_exempt
def car_size_exist(payload):
    """renvoi la categorie de la voiture"""
    name_car_size = payload.get('car_size')
    if name_car_size is None:
        return (None)
    else:
        size = {'petite voiture': '1',
            'moyenne voiture': '2',
            'grande voiture': '3'
            }
        return size[name_car_size]

@csrf_exempt
def post_user(request):
    #try:
    data = json.loads(request.body.decode())
    for i in range(0, len(data)):
        payload = data[i]
        print(payload)
        if User.objects.filter(email=payload['email']).exists():
            return HttpResponse(status=400)

        new_user = User(
            email=test_email(payload),
            first_name=payload.get('first_name'),
            last_name=payload.get('last_name'),
            user_img=payload.get('user_img', None),
            is_active=payload.get('is_active', True),
            is_staff=payload.get('is_staff', False),
            user_permission=payload.get('user_permission', 0),
            date_birth=payload.get('date_bitrh', None),
            social_professional_category=csp_exist(payload),
            gender=gender_exist(payload),
            phone_number=payload.get('phone_number', None),
            car_size=car_size_exist(payload),
            home_address_id=address_exist(payload)
        )

        new_user.set_password(payload.get('password'))
        new_user.save()

        if payload.get('name_center_of_interest'):
            for CenterOfInterest in payload.get('name_center_of_interest'):
                    new_InterestFor = InterestFor(
                        user_id=User.objects.get(email=payload['email']).id,
                        center_of_interest_id=CenterOfInterest_exist(CenterOfInterest)
                    )
                    new_InterestFor.save()

    return HttpResponse(status=201)
    # except:
    #     return HttpResponse(status=400)
