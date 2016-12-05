from rest_framework import serializers

from .models import Item
from .models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'join_date'
        )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'pub_date',
            'pub_person'
        )
