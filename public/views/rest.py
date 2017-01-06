# from rest_framework import permissions, viewsets

# from public.models import (
#     Item,
#     User
# )
# from public.paginations import ItemViewSetPagination
# from public.permissions import IsStaffOrTargetUser
# from public.serializers import (
#     ItemSerializer,
#     UserSerializer
# )


# class ItemViewSet(viewsets.ModelViewSet):

#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#     pagination_class = ItemViewSetPagination


# class UserViewSet(viewsets.ModelViewSet):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'email'

    #def get_permissions(self):
    #   # Allow non-authenticated user to create via POST
    #   return [permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()]
