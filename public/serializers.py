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
            'username',
            'password'
        )
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_model = get_user_model()
        password = validated_data.pop('password')
        user = user_model.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password') if 'password' in validated_data else None
        for k, v in validated_data.items():
            instance[k] = v
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
