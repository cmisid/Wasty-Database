from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Advert,
    User,
    Category,
    SubCategory,
    Recovery
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'date_joined',
            'email',
            'last_name',
            'first_name',
            'user_img',
            'user_img_placeholder',
            'password',
            'gender',
            'date_birth',
            'social_professional_category',
            'phone_number',
            'home_address',
            'user_permission',
        )
        read_only_fields = (
            'date_joined',
            'date_unsubscribe'
            'user_img_placeholder',
            'user_permission',
            'last_login',
            'user_location',
        )

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.create(**validated_data)
        password = validated_data.pop('password')
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


class AdvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advert
        fields = (
            'title',
            'advert_date',
            'advert_state',
            'situation',
            'price',
            'type_place',
            'description',
            'advert_img',
            'advert_img',
            'advert_img',
            'advert_img_placeholder',
            'object_state',
            'volume',
            'weight',
            'quantity',
            'forecast_time',
            'forecast_price',
            'buy_place',
            'advert_user',
            'advert_address',
            'sub_category',

        )
        read_only_fields = (
            'advert_date',
            'forecast_time',
            'forecast_price',
            'advert_user',
            'advert_address',
            'sub_category',

        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'category_name',
        )


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = (
            'sub_category_name',
            'category',

        )
        read_only_fields = (
            'catagory',
        )


class RecoverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Recovery
        fields = (
            'recovery_datetime',
            'recovery_user',
            'advert',
        )
        read_only_fields = (
            'recovery_datetime',
        )