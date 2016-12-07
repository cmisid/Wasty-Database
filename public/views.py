from rest_framework import permissions, viewsets

from .models import (
    Item,
    User
)

from .serializers import (
    ItemSerializer,
    UserSerializer
)


class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [
        permissions.AllowAny # Or else anon users can't register
    ]
