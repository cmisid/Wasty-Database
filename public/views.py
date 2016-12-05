from rest_framework import viewsets

from .models import (
    Item,
    Person
)

from .serializers import (
    ItemSerializer,
    PersonSerializer
)


class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
