from rest_framework import permissions, viewsets

from .models import (
    Item,
    User
)
from .permissions import IsStaffOrTargetUser
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
    lookup_field = 'email'

    #def get_permissions(self):
    #   # Allow non-authenticated user to create via POST
    #   return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]
