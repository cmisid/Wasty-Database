from django.conf.urls import include, url
from rest_framework import routers

from .views import base
from .views import custom
from .views import rest
from .views import custom_get_G4 as G4
from .views import custom_get_G2 as G2
from .views import custom_post_user, custom_post_advert
from .views import custom_post_pickup_point


router = routers.DefaultRouter()

router.register(r'^adverts', rest.AdvertViewSet)
router.register(r'^users', rest.UserViewSet)
router.register(r'^categories', rest.CategoryViewSet)
router.register(r'^subcategories', rest.SubCategoryViewSet)
router.register(r'^recoveries', rest.RecoveryViewSet)
router.register(r'^interestfor', rest.InterestForViewSet)
router.register(r'^centersofinterest', rest.CenterOfInterestViewSet)
router.register(r'^cities', rest.CityViewSet)
router.register(r'^districts', rest.DistrictViewSet)
router.register(r'^addresses', rest.AddressViewSet)
router.register(r'^visits', rest.VisitViewSet)
router.register(r'^likes', rest.LikeViewSet)
router.register(r'^pickuppoints', rest.PickUpPointViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ping', base.ping),
    url(r'^get-user/(?P<user_id>[0-9]+)/$', custom.get_user, name='get_user'),
    url(r'^nb_user/', G4.nb_user_get, name='nb_user'),
    url(r'^evolution_users_number_users/', G4.evolution_users_number_users, name='evolution_users_number_users'),
    url(r'^visit_and_likes/(?P<id>[0-9]+)/$', G2.visit_and_likes, name='visit_and_likes' ),
    url(r'^get_annonce_valide/(?P<id_cat>[0-9]+)/$', G2.get_annonce_valide, name='get_annnce_valide' ),
    url(r'^get_nb/(?P<id_advert>[0-9]+)/$', G2.get_nb, name='get_nb' ),

#url G2 G5

    url(r'^post_user$', custom_post_user.post_user, name='post_user'),
    url(r'^post_pickup_point$', custom_post_pickup_point.post_pickup_point, name='post_pickup_point')

]
