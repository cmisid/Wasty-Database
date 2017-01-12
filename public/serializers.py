from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
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
            'last_login',
            'car_size',
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
            'advert_img_placeholder',
            'object_state',
            'volume',
            'weight',
            'quantity',
            'buy_place',
            'advert_user',
            'advert_address',
            'sub_category',
            'constraint_time_begin',
            'constraint_time_end',

        )
        read_only_fields = (
            'advert_date',
            'forecast_time',
            'forecast_price',
            'advert_img_placeholder',
            'advert_address',
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


class InterestForSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestFor
        fields = (
            'user',
            'center_of_interest',
        )


class CenterOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterOfInterest
        fields = (
            'name_center_of_interest',
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'city_name',
        )


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            'district_name',
            'city',
            'density',
            'polygon',
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'street_number',
            'street_name',
            'postal_code',
            'district',
            'address_city',
            'complement',
            'location',
        )
        read_only_fields = (
            'location',
        )


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = (
            'advert_visit',
            'user_visit',
            'visit_datetime'
        )
        read_only_fields = (
            'visit_datetime',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'advert_like',
            'user_like',
            'like_datetime'
        )
        read_only_fields = (
            'like_datetime',
        )


class PickUpPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickUpPoint
        fields = (
            'pickup_point_address',
            'recovery_type',
        )