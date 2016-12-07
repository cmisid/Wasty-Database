from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Item,
    User
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'password'
        )

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_model = get_user_model()
        password = validated_data.pop('password')
        user = user_model.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
