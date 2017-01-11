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


# def users_number_users_year_get(request, pyear): 
#     """ Donne le nombre d utilisateurs ayant créés un compte cette année."""
#     result = []
#     try:
#         cur = connection.cursor()
#         cur.execute("""
#            SELECT
#                count(id)
#             FROM
#                 t_users
#             WHERE
#                 pyear >= year(date_joined);
#         """)
#         columns = ['n_user_year']
#         print(columns)
#         for row in cur.fetchall():
#             result.append(dict(zip(columns, row)))
#         return HttpResponse(json.dumps(result, indent=2))
#     except:
#         return HttpResponse(status=400)

#extract(year from date(date_joined)))
def evolution_users_number_users(request):
    """ Donne le nombre d utilisateurs ayant créés un compte cette année."""
    result = []
    try:
        cur = connection.cursor()
        cur.execute("""
            SELECT
                SUBSTR(to_char(extract(year from date(date_joined))),1,1) , id
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


