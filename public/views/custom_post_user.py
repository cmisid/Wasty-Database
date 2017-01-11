import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.gis.geos import Point

from public.models import User, Address, City, CenterOfInterest, InterestFor, District
from public import modify_address

@csrf_exempt
def city_exist(payload):
    """recherche de la city ajoute dans la bd"""
    city_name = payload.get('city_name')
    if not City.objects.filter(city_name=city_name).exists():
        city = City(city_name=city_name).save()
    else:
        city = City.objects.get(city_name=city_name)
    return(city.id)

@csrf_exempt
def district_exist(payload):
    name_district = payload.get('district')
    print(name_district)
    if name_district is None:
        return (None)
    else:
        district = {'NULL' : '0',
                'CAPITOLE' : '1',
                'SAINT-GEORGES' : '2',
                'JUNCASSE - ARGOULETS' : '3',
                'GRAMONT' : '4',
                'LA TERRASSE' : '5',
                'ZONES D\'ACTIVITES SUD' : '6',
                'FONTAINE-LESTANG' : '7',
                'PONT-DES-DEMOISELLES' : '8',
                'PATTE D\'OIE' : '9',
                'LE BUSCA' : '10',
                'CROIX-DE-PIERRE' : '11',
                'REYNERIE' : '12',
                'MATABIAU' : '13',
                'FAOURETTE' : '14',
                'SAINT-ETIENNE' : '15',
                'SAINT-SIMON' : '16',
                'LES IZARDS' : '17',
                'SAINT-MARTIN-DU-TOUCH' : '18',
                'LES CHALETS' : '19',
                'LARDENNE' : '20',
                'ARENES' : '21',
                'AMIDONNIERS' : '22',
                'MIRAIL-UNIVERSITE' : '23',
                'LES PRADETTES' : '24',
                'COMPANS' : '25',
                'GINESTOUS' : '26',
                'SAINT-MICHEL' : '27',
                'FER-A-CHEVAL' : '28',
                'BELLEFONTAINE' : '29',
                'SOUPETARD' : '30',
                'PAPUS' : '31',
                'POUVOURVILLE' : '32',
                'BASSO-CAMBO' : '33',
                'ARNAUD BERNARD' : '34',
                'SAINT-AUBIN - DUPUY' : '35',
                'JULES JULIEN' : '36',
                'CROIX-DAURADE' : '37',
                'CASSELARDIT' : '38',
                'MINIMES' : '39',
                'RAMIER' : '40',
                'LA CEPIERE' : '41',
                'EMPALOT' : '42',
                'LALANDE' : '43',
                'RANGUEIL - CHR - FACULTES' : '44',
                'CARMES' : '45',
                'LA FOURGUETTE' : '46',
                'BARRIERE-DE-PARIS' : '47',
                'MONTAUDRAN - LESPINET' : '48',
                'SAINT-AGNE' : '49',
                'PURPAN' : '50',
                'SAUZELONG - RANGUEIL' : '51',
                'SAINT-CYPRIEN' : '52',
                'BAGATELLE' : '53',
                'GUILHEMERY' : '54',
                'MARENGO - JOLIMONT' : '55',
                'COTE PAVEE' : '56',
                'CHATEAU-DE-L\'HERS' : '57',
                'ROSERAIE' : '58',
                'BONNEFOY' : '59',
                'SEPT DENIERS' : '60'
                }
        new_district = District(district_name=district[name_district],
                                city_id=city_exist(payload)).save()
        print(city_exist(payload))
        print("coucou", new_district)
    return (None)

@csrf_exempt
def address_exist(payload):
    """cherche si l'adresse existe dans la bd si oui renvoi l'id sinon la creee"""
    a_number = payload.get('street_number')
    a_name = payload.get('street_name')
    a_cp = payload.get('postal_code')
    a_complement = payload.get('complement', None)
    if not Address.objects.filter(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement).exists():
            new_address = Address(
                street_number=a_number,
                street_name=a_name,
                postal_code=a_cp,
                address_city_id=city_exist(payload),
                #district_id=district_exist(payload),
                location=Point(modify_address.geocoder((a_number, a_name, a_cp, payload.get('city_name'))))
            )
            address = new_address.save()
    else:
        address = Address.objects.get(street_number=a_number, street_name=a_name, postal_code=a_cp, complement=a_complement)

        return(address.id)


@csrf_exempt
def test_email(payload):
    email = payload.get('email')
    if not User.objects.filter(email=email).exists():
        return email
    else:
        return HttpResponse(status=400)

@csrf_exempt
def CenterOfInterest_exist(CenterInterest):
    print(CenterInterest)
    if CenterInterest is None:
        return 'ERROR'
    else:
        center = {'sport': '1',
        'theatre': '2',
        'cinema': '3',
        'voyage': '4',
        'musique': '5',
        'jeux_videos': '6',
        'informatique': '7',
        'recyclage': '8',
        'jardinage': '9',
        'animaux': '10',
        'photographie': '11',
        'lecture': '12',
        'peinture': '13',
        'decoration_interieure': '14',
        'peche': '15',
        'camping': '16',
        'mode': '17',
        'chasse': '18',
        'automobile': '19',
        'cuisine': '20',
        'autres': '21'
        }
        new_center = CenterOfInterest(name_center_of_interest=1).save()
        print(new_center)
        return (new_center.id)


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
    payload = json.loads(request.body.decode())
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

    # for CenterOfInterest in payload.get('name_center_of_interest'):
    #         new_InterestFor = InterestFor(
    #             user_id=new_user.id,
    #             center_of_interest_id=CenterOfInterest_exist(CenterOfInterest)
    #         )
    #         new_InterestFor.save()

    return HttpResponse(status=201)
    # except:
    #     return HttpResponse(status=400)
