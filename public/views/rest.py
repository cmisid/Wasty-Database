from rest_framework import permissions, viewsets

from public.models import (
	Advert,
	User,
	Category,
	SubCategory,
	Recovery
)

from public.paginations import AdvertViewSetPagination
from public.permissions import IsStaffOrTargetUser
from public.serializers import (
	AdvertSerializer,
	UserSerializer,
	CategorySerializer,
	SubCategorySerializer,
	RecoverySerializer
)


class AdvertViewSet(viewsets.ModelViewSet):

	queryset = Advert.objects.all()
	serializer_class = AdvertSerializer
	pagination_class = AdvertViewSetPagination


class UserViewSet(viewsets.ModelViewSet):

	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'email'


class CategoryViewSet(viewsets.ModelViewSet):

	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	pagination_class = AdvertViewSetPagination


class SubCategoryViewSet(viewsets.ModelViewSet):

	queryset = SubCategory.objects.all()
	serializer_class = SubCategorySerializer
	pagination_class = AdvertViewSetPagination


class RecoveryViewSet(viewsets.ModelViewSet):

	queryset = Recovery.objects.all()
	serializer_class = RecoverySerializer
	pagination_class = AdvertViewSetPagination

	#def get_permissions(self):
	#	# Allow non-authenticated user to create via POST
    #   	return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]
