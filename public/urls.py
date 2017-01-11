from django.conf.urls import include, url
from rest_framework import routers

from .views import base
from .views import custom
from .views import rest
from .views import custom_get_G4 as G4
from .views import custom_post_user


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
 #  url(r'^nb_user_year/(?P<user_id>[0-9]+)/$', G4.users_number_users_year_get, name='users_number_users_year_get'),
    url(r'^evolution_users_number_users/', G4.evolution_users_number_users, name='evolution_users_number_users'),
 #   url(r'^post-advert', custom.post_advert, name='post_advert'),
    url(r'^post_user$', custom_post_user.post_user, name='post_user')

]
