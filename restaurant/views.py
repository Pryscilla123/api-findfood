from django.shortcuts import render
from .serializers import RestaurantSerializer, AddressSerializer, RestaurantInformationSerializer, ScheduleSerializer
from .models import Restaurant, Address, Schedule
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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RestaurantInformationViewSet(ListModelMixin, GenericViewSet):
    """
    Rota das Informações dos Restaurantes.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantInformationSerializer
