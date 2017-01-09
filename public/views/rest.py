from rest_framework import permissions, viewsets

from public.models import (
	Advert,
	User,
	Category,
	SubCategory,
	Recovery,
	InterestFor,
	CenterOfInterest,
	City,
	District,
	Address,
	Visit,
	Like,
	PickUpPoint
)

from public.paginations import AdvertViewSetPagination
from public.permissions import IsStaffOrTargetUser
from public.serializers import (
	AdvertSerializer,
	UserSerializer,
	CategorySerializer,
	SubCategorySerializer,
	RecoverySerializer,
	InterestForSerializer,
	CenterOfInterestSerializer,
	CitySerializer,
	DistrictSerializer,
	AddressSerializer,
	VisitSerializer,
	LikeSerializer,
	PickUpPointSerializer
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


class InterestForViewSet(viewsets.ModelViewSet):

	queryset = InterestFor.objects.all()
	serializer_class = InterestForSerializer


class CenterOfInterestViewSet(viewsets.ModelViewSet):

	queryset = CenterOfInterest.objects.all()
	serializer_class = CenterOfInterestSerializer


class DistrictViewSet(viewsets.ModelViewSet):

	queryset = District.objects.all()
	serializer_class = DistrictSerializer


class CityViewSet(viewsets.ModelViewSet):

	queryset = City.objects.all()
	serializer_class = CitySerializer


class VisitViewSet(viewsets.ModelViewSet):

	queryset = Visit.objects.all()
	serializer_class = VisitSerializer


class AddressViewSet(viewsets.ModelViewSet):

	queryset = Address.objects.all()
	serializer_class = AddressSerializer


class LikeViewSet(viewsets.ModelViewSet):

	queryset = Like.objects.all()
	serializer_class = LikeSerializer


class PickUpPointViewSet(viewsets.ModelViewSet):

	queryset = PickUpPoint.objects.all()
	serializer_class = PickUpPointSerializer


	#def get_permissions(self):
	#	# Allow non-authenticated user to create via POST
    #   	return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]
