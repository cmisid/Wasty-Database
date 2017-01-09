from django.conf.urls import include, url
from rest_framework import routers

from .views import base
from .views import rest


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
    url(r'^ping', base.ping)
]
