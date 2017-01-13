import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from public.models import User, Address, City


def nb_user_get(request):
    """nb utilisateurs dans la bd"""
    try:
        cur = connection.cursor()
        cur.execute("""
           SELECT
                count(id)
            FROM
                t_users
        """)
        columns = ['n_users']
        result = cur.fetchall()[0]
        return JsonResponse(dict(zip(columns, result)))
    except:
        return HttpResponse(status=400)


def evolution_users_number_users(request):
    """ Donne le nombre d utilisateurs ayant créés un compte cette année."""
    result = []
    try:
        cur = connection.cursor()
        cur.execute("""
            SELECT
                extract(year from date(date_joined)) , id
            FROM
                t_users
        """)
        print("coucou")
        columns = ['year', 'count']
        for row in cur.fetchall():
            result.append(dict(zip(columns, row)))
        print(result)
        return HttpResponse(json.dumps(result, indent=2))
    except:
        return HttpResponse(status=400)
