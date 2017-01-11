import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from public.models import User, Address, City, CenterOfInterest, InterestFor, District
from public import modify_address


def city_exist(payload):
    """recherche de la city ajoute dans la bd"""
    city_name = payload.get('city_name')

    if not City.objects.filter(city_name=city_name).exists():
        city = City(city_name=city_name).save()
    else:
        city = City.objects.get(city_name=city_name)
    return(city.id)


def district_exist(payload):
    try:
        district_name = payload.get('district_name')
        return(District.objects.get(district_name=district_name).id)
    except:
        return HttpResponse(status=400)


def address_exist(payload):
    """cherche si l'adresse existe dans la bd si oui renvoi l'id sinon la creee"""
    a_number = payload.get('street_number'),
    a_name = payload.get('street_name'),
    a_cp = payload.get('postal_code'),
    a_complement = payload.get('complement'),

    if not Address.objects.filter(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement).exists():
        new_address = Address(
            street_number=a_number,
            street_name=a_name,
            postal_code=a_cp,
            address_city=city_exist(payload),
            district=district_exist(payload),
            location=modify_address.geocoder(a_number, a_name, a_cp, City.objects.get(id=address_city).city_name)
        )
        address = new_address.save()
    else:
        address = Address.objects.get(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement)

    return(address.id)


def test_email(payload):
    email = payload.get('email')
    if not User.objects.filter(email=email).exists():
        return email
    else:
        return HttpResponse(status=400)


def CenterOfInterest_exist(CenterInterest):
    if CenterOfInterest.object.filter(name_center_of_interest=CenterInterest).exists():
        return(CenterOfInterest.object.get(name_center_of_interest=CenterInterest).id)
    else:
        return HttpResponse(status=400)


@csrf_exempt
def gender_exist(payload):
    name_gender = payload.get('gender')
    g = {'Homme': 'M', 'Femme': 'F'}
    return g[name_gender]

@csrf_exempt
def post_user(request):
    #try:
    payload = json.loads(request.body.decode())
    print(payload.get('gender'))
    if User.objects.filter(email=payload['email']).exists():
        return HttpResponse(status=400)

    new_user = User(
        email=test_email(payload),
        #password=set_password(self.payload.get('password')),
        first_name=payload.get('first_name'),
        last_name=payload.get('last_name'),
        user_img=payload.get('user_img', null),
        is_active=payload.get('is_active', True),
        is_staff=payload.get('is_staff', False),
        user_permission=payload.get('user_permission', 0),
        # date_birth=payload.get('date_bitrh'),
        #social_professional_category=payload.get('social_professional_category'),
        gender=gender_exist(payload),
        #phone_number=payload.get('phone_number'),
        # car_size=payload.get('car_size'),
        # home_address=address_exist(payload)
    )

    new_user.save()

    # for CenterOfInterest in payload.get('name_center_of_interest'):
    #         new_InterestFor = InterestFor(
    #             user=new_user.id,
    #             center_of_interest=CenterOfInterest_exist(CenterOfInterest)
    #         )
    #         new_InterestFor.save()

    return HttpResponse(status=201)
    # except:
    #     return HttpResponse(status=400)
