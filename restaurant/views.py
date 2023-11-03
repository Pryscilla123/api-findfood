from django.shortcuts import render
from .serializers import RestaurantSerializer, AddressSerializer, RestaurantInformationSerializer, ScheduleSerializer
from .models import Restaurant, Address, Schedule, Interval
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


# Create your views here.


class RestaurantViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete do Restaurante.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class AddressViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete do Endereço do restaurante.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ScheduleViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete dos Horários de funcionamento do restaurante.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'interval_id__day'

    def create(self, request, *args, **kwargs):
        """
        Estrutura -> List[dict]
        Estrutura do dict ->
        {
            "schedule": {
                "day": str,
                "open": str,
                "close": str
            },
            "restaurant_id": int
        },
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        intervals = self._create_interval(request.data)
        serializer = self.serializer_class(data=intervals, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        interval = self._interval_to_update(request.data)
        schedule = list(Schedule.objects.filter(**kwargs)).pop(0)
        schedule.interval_id = interval
        schedule.save()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def _create_interval(data):
        schedule = []
        for interval in data:
            day = interval.get('schedule')
            interval_obj = Interval.objects.filter(**day)
            if not interval_obj:
                new_interval_obj = Interval.objects.create(**day)
                schedule.append({'restaurant_id': interval.get('restaurant_id'), 'interval_id': new_interval_obj.id})
            else:
                existing_interval_obj = list(interval_obj).pop(0)
                schedule.append(
                    {'restaurant_id': interval.get('restaurant_id'), 'interval_id': existing_interval_obj.id})
        return schedule

    @staticmethod
    def _interval_to_update(data):
        interval = Interval.objects.filter(**data)

        if not interval:
            new_interval_obj = Interval.objects.create(**data)
            return new_interval_obj
        else:
            return list(interval).pop(0)


class RestaurantInformationViewSet(ListModelMixin, GenericViewSet):
    """
    Rota das Informações dos Restaurantes.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantInformationSerializer
