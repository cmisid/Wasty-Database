import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from public.models import User, Address, City
from views import custom_post_user
from public import modify_address


def user_exist(payload):
    email = payload.get('email')
    if User.objects.filter(email=email).exists():
        return(User.objects.get(email=email).id)
    else
        return HttpResponse(status=400)


def advert_address_exist(payload):
    if 'location' in payload:
        location = payload.get('location')
        if Address.objects.filter(location=location).exists():
            return(Address.objects.get(location=location).id)
        else:
            (a_number, a_name, a_cp, city) = modify_address.geocoder_inverse(location)
            new_address = Address(
                street_number=a_number,
                street_name=a_name,
                postal_code=a_cp,
                address_city=custom.post_user.city_exist(city),
                district=custom.post_user.district_exist(payload),
                location=location
            )
            address = new_address.save()
            return(address.id)
    elif 'street_number', 'street_name' in payload:
        return(custom_post_user.address_exist(payload))
    else:
        return 'ERROR'


def sub_category_exist():
    



def post_advert(request):
    try:
        payload = json.loads(request.body)
        advert = Advert(
            title=payload.get('title'),
            advert_state=payload.get('advert_state'),
            situation=payload.get('situation'),
            price=payload.get('price'),
            type_place=payload.get('type_place'),
            description=payload.get('description'),
            advert_img=payload.get('advert_img'),
            object_state=payload.get('object_state'),
            volume=payload.get('volume'),
            weight=payload.get('weight'),
            quantity=payload.get('quantity', 1),
            buy_place=payload.get('buy_place'),
            constraint_time_begin=payload.get('constraint_time_begin'),
            constraint_time_end=payload.get('constraint_time_end'),
            advert_user=user_exist(payload),
            advert_address=advert_address_exist(payload),
            sub_category=sub_category_exist(payload),
        )

        advert.save()
        return HttpResponse(status=201)
    except:
        return HttpResponse(status=400)
