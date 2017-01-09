import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def post_advert(request):
    try:
        payload = json.loads(request.body)
        advert = Advert(
            title=payload['title']
        )
        advert.save()
        return HttpResponse(status=201)
    except:
        return HttpResponse(status=400)
