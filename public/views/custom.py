from django.http import HttpResponse

from public.models import User


def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return HttpResponse(status=400)
