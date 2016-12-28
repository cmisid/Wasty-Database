from django.conf.urls import include, url
from rest_framework import routers

from .views import base
from .views import rest


router = routers.DefaultRouter()

router.register(r'items', rest.ItemViewSet)
router.register(r'users', rest.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ping', base.ping)
]
