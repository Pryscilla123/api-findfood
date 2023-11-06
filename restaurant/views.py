from django.shortcuts import render
from .serializers import RestaurantSerializer, AddressSerializer, RestaurantInformationSerializer, ScheduleSerializer, \
    ContactSerializer
from .models import Restaurant, Address, Schedule, Contact
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response


# Create your views here.


class RestaurantViewSet(ModelViewSet):
    """
    Rota de create, update e delete do Restaurante.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RestaurantInformationSerializer
        return RestaurantSerializer


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
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete para as formas de contato do restaurant.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

