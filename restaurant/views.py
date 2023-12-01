from .serializers import RestaurantSerializer, AddressSerializer, RestaurantInformationSerializer, ScheduleSerializer, \
    ContactSerializer
from .models import Restaurant, Address, Schedule, Contact
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from django.db.models import Q
from utils.tools import Days
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.


class RestaurantViewSet(ModelViewSet):
    """
    Rota de create, update e delete do Restaurante.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'type', 'restaurant_address__line1', 'restaurant_address__line2',
                        'restaurant_address__postal_code']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        is_open = self.request.query_params.get('is_open', None)

        if is_open == 'true':
            queryset = Restaurant.objects.filter(Q(opening_days__interval_id__open__lte=datetime.now().time()) & Q(
                opening_days__interval_id__close__gte=datetime.now().time()) & Q(
                opening_days__interval_id__day__exact=Days[datetime.now().strftime('%A').upper()].value))
        elif is_open == 'false':
            queryset = Restaurant.objects.exclude(Q(opening_days__interval_id__open__lte=datetime.now().time()) & Q(
                opening_days__interval_id__close__gte=datetime.now().time()) & Q(
                opening_days__interval_id__day__exact=Days[datetime.now().strftime('%A').upper()].value))

        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RestaurantInformationSerializer
        return RestaurantSerializer


class AddressViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete do Endereço do restaurante.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class ScheduleViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Rota de create, update e delete dos Horários de funcionamento do restaurante.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
