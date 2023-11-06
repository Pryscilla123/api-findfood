from .models import Restaurant, Address, Schedule, Interval, Contact
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


class IntervalSerializer(ModelSerializer):

    class Meta:
        model = Interval
        fields = ['id', 'day', 'open', 'close']


class ScheduleSerializer(ModelSerializer):

    interval_id = IntervalSerializer()

    class Meta:
        model = Schedule
        fields = ['id', 'interval_id', 'restaurant_id']
        extra_kwargs = {
            'restaurant_id': {'write_only': True}
        }

    def create(self, validated_data):
        interval_id = validated_data.pop('interval_id')
        interval = self._get_or_create_interval(dict(interval_id))
        schedule = Schedule.objects.create(interval_id=interval, **validated_data)
        return schedule

    def update(self, instance, validated_data):
        interval_id = validated_data.pop('interval_id')
        interval = self._get_or_create_interval(dict(interval_id))
        instance.interval_id = interval
        instance.save()

        return instance

    @staticmethod
    def _get_or_create_interval(data):
        interval_obj = Interval.objects.filter(**data)
        if not interval_obj:
            interval = Interval.objects.create(**data)
        else:
            interval = list(interval_obj).pop(0)
        return interval


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = ['type', 'information', 'restaurant_id']
        extra_kwargs = {
            'restaurant_id': {'write_only': True}
        }


class RestaurantInformationSerializer(ModelSerializer):

    restaurant_address = AddressSerializer(read_only=True)
    opening_days = ScheduleSerializer(read_only=True, many=True)
    socials = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'type', 'restaurant_address', 'opening_days', 'socials', 'img']
