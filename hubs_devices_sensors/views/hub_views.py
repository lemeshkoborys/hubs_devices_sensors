from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
import hubs_devices_sensors.serializers as serializers
from hubs_devices_sensors.models import Sensor, Device, Hub, SensorCollectedData


class HubListAPIView(generics.ListAPIView):

    """
    Class Based View for LIST serialized Hub objects
    @param permission_classes - permission classes for this Class Based View

    ALLOWED_METHODS: GET
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.HubModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Hub.objects.filter(owner=user)


class HubCreateAPIView(generics.CreateAPIView):

    """
    Class Based View for CREATE serialized Hub objects
    @param permission_classes - permission classes for this Class Based View

    @method perform_create - automatically adds owner to Hub object on create
    ALLOWED_METHODS: POST
    """

    permission_classes = (IsAuthenticated, )

    queryset = Hub.objects.all()
    serializer_class = serializers.HubModelSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HubRetrieveUpateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    """
    Class Based View HubRetrieveUpateDestroyAPIView
    Allows to Retrieve Update and Destroy single Hub object
    @param permission_classes - permission classes for this Class Based View

    ALLOWED METHODS - GET, PUT, PATCH, DELETE
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.HubModelSerializer

    def get_queryset(self):
        user = self.request.user

        hub = Hub.objects.filter(pk=self.kwargs['pk'])

        try:
            if hub.first().owner == user:
                return hub
            else:
                raise exceptions.PermissionDenied('You are not allowed to perform this action')
        except AttributeError:
            raise exceptions.NotFound('Requested Hub was not found at our own')


class HubDevicesListAPIView(generics.ListAPIView):

    """
    ClassBasedView that lists all Device entities related to Hub
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.HubModelSerializer

    def get_queryset(self):
        return Device.objects.filter(
            device_hub=Hub.objects.get(pk=self.kwargs['pk'])
        )