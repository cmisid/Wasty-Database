import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from public.models import Advert, User


def get_user(request, user_id):
    """recupere les infos d'un user"""
    try:
        user = User.objects.get(pk=user_id)
        print(user)
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


def get_post_users(request, id):
	""""recupere les annonces valide recupere et supprimer d un user"""
	try:
		adverts = Advert.objects.filter(advert_user_id=id)
		return JsonResponse({
			'adverts': [
				{
					'advert_id': ad.title
				}
			for ad in adverts
			if ad.advert_state in ('1', '3', '4')
		]})
	except:
		return HttpResponse(status=400)


def get_annonce_valide(request, id_cat):
    """Recupere les annonces valide ayant une categorie donnee"""
    try:
        liste_res=[]
        
        category = SubCategory.objects.filter(category_id=id_cat)
        
        for cat in category.all():
        
            sub_category= cat.id
            
            state=(Advert.objects.get(sub_category_id=sub_category)).advert_state
            id_annonce = (Advert.objects.get(sub_category_id=sub_category))
            
            if state=='4':
                dic_res={}
                dic_res['advert_id']=id_annonce.id
                dic_res['title']=id_annonce.title
                dic_res['advert_state']=id_annonce.advert_state
                dic_res['situation']=id_annonce.situation
                dic_res['price']=id_annonce.price
                dic_res['type_place']=id_annonce.type_place
                dic_res['description']=id_annonce.description
                dic_res['object_state']=id_annonce.object_state
                
                dic_res['volume']=id_annonce.volume
                
                dic_res['weight']=id_annonce.weight
                
                dic_res['quantity']=id_annonce.quantity
                
                dic_res['buy_place']=id_annonce.buy_place
                dic_res['advert_address_id']=id_annonce.advert_address_id
                dic_res['advert_user_id']=id_annonce.advert_user_id
                dic_res['sub_category_id']=id_annonce.sub_category_id
                liste_res.append(dic_res)
        return HttpResponse(json.dumps(liste_res, indent=2))
    except:
        return HttpResponse(status=400)


def visit_and_likes(request, id):
    """Recupere les pages likees et visitees par un user"""
    try:
        if Like.objects.filter(user_like_id=id).exists():
            user_like=Like.objects.get(user_like_id=id)
            return JsonResponse({        
                        'advert_like': user_like.advert_like_id,
                        'user_like': user_like.user_like_id,
                        'like_datetime' : user_like.like_datetime,
                        'parametre' : 1,
                    })
        else:
            user_visit=Visit.objects.get(user_visit_id=id)
            return JsonResponse({
                
                        'advert_visit': user_visit.advert_visit_id,
                        'user_visit': user_visit.user_visit_id,
                        'visit_datetime' : user_visit.visit_datetime,
                        'parametre' : 0,
                    
                })
    except:
        return HttpResponse(" L'utilisateur n'a visité ou liké aucune page")


def get_annonces(request):
    """Recupere les 20 annonces publies les plus recentes et valide"""
    advert=Advert.objects.order_by('advert_date')[:20]
    return JsonResponse({
        'advert': [
            {
                'advert-id': item.id,
                'advert_id'  : item.id,
                'title'  : item.title,
                'advert_date'  : item.advert_date,
                'advert_state'  : item.advert_state,
                'situation'  : item.situation,
                'price'  : item.price,
                'type_place'  : item.type_place,
                'description'  : item.description,
                'object_state'  : item.object_state,
                'volume'  : item.volume,
                'weight'  : item.weight,
                'quantity'  : item.quantity,
                'buy_place'  : item.buy_place,
                'advert_address_id'  : item.advert_address_id,
                'advert_user_id'  : item.advert_user_id,
                'sub_category_id'  : item.sub_category_id,
                'constraint_time_begin'  : item. constraint_time_begin,
                'constraint_time_end'  : item.constraint_time_end,
            }
            for item in advert
            if item.id
        ]
    })


def get_nb(request, id_advert):
    """Recupere le nombre de likes et de visites d'une annonce"""
    try:
        advert_visit=Visit.objects.filter(advert_visit_id=id_advert).count()
        
        advert_like=Like.objects.filter(advert_like_id=id_advert).count()

        return JsonResponse({
            'advert_id' : id_advert,
            'count visit' : advert_visit,
            'count like' : advert_like,
        
        })
    except:
        return HttpResponse(statut=400)
