from .models import Restaurant, Address, Schedule
from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField, IntegerField


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'line1', 'line2', 'number', 'postal_code', 'restaurant_id']
        extra_kwargs = {
            'restaurant_id': {'write_only': True}
        }


class RestaurantSerializer(ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'type', 'img']


class ScheduleSerializer(ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['id', 'day', 'open', 'close', 'restaurant_id']
        extra_kwargs = {
            'restaurant_id': {'write_only': True}
        }


class RestaurantInformationSerializer(ModelSerializer):

    restaurant_address = AddressSerializer(read_only=True)
    opening_days = ScheduleSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'type', 'restaurant_address', 'opening_days', 'img']
