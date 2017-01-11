import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from public.models import Advert
from public.models import User


def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        home_address = user.home_address
        return JsonResponse({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': {
                'street_name': home_address.street_name,
                'street_number': home_address.street_number
            }
        })
    except:
        return HttpResponse(status=400)


# @csrf_exempt
# def post_advert(request):
#     try:

#       #  if 'latitude' in payload:

#         payload = json.loads(request.body)

#         #if 'advert_state' in payload:
            
#         new_advert = Advert(
#     #       title = payload.get('latitude'),
#             title=payload['title'],
#             advert_date=payload['advert_date'],
#             advert_state=payload['advert_state'],
#             situation=payload['situation'],
#             price=payload['price'],
#             type_place=payload['type_place'],
#             description=payload['description'],
#             advert_img=payload['advert_img'],
#             advert_img_placeholder=payload['advert_img_plaaceholder'],
#             object_state=payload['object_state'],
#             volume=payload['volume'],
#             weight=payload['weight'],
#             quantity=payload['quantity'],
#             buy_place=payload['buy_place'],
#             constraint_time_begin=payload['constraint_time_begin'],
#             constraint_time_end=payload['constraint_time_end'],
#             advert_user=payload['advert_user'],
#             advert_address=payload['advert_address'],
#             sub_category=payload['sub_category'],
#         )
#         new_advert.save()
#        # advert.id
#         return HttpResponse(status=201)
#     except:
#         return HttpResponse(status=400)


# def post_user(request):
#     try:
#         payload = json.loads(request.body)
#         user = User(
#             date_joinded=payload['Date joined'],
#             email=payload['Email address'],
#             first_name=payload['First name'],
#             user_img=payload['User img'],
#             last_name=payload['First name'],
#         )


# def nb_user(request):
#     try:
#         cur = connection.cursor()
#         cur.execute("""
#            SELECT
#                 count(id)
#             FROM
#                 t_users
#         """)
#         columns = ['n_users']
#         result = cur.fetchall()[0]
#         return JsonResponse(dict(zip(columns, result)))
#     except:
#         return HttpResponse(status=400)


def nb_user(request):
    result = []
    try:
        cur = connection.cursor()
        cur.execute("""
           SELECT
               id, first_name, last_name
            FROM
                t_users;
        """)
        columns = ['id', 'first_name', 'last_name']
        print(columns)
        for row in cur.fetchall():
            result.append(dict(zip(columns, row)))
        return HttpResponse(json.dumps(result, indent=2))
    except:
        return HttpResponse(status=400)
