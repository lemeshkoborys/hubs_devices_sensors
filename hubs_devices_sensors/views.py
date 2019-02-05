"""
views.py
Classes:
    SensorListCreateAPIView,
    DeviceListCreateAPIView,
    HubListAPIView,
    HubCreateAPIView,
    SensorCollectedDataListCreateAPIView,
    SensorCollectedDataAdminAPIView,
    SensorCollectedDataUserAPIView
"""
from .models import Sensor, Device, Hub, SensorCollectedData
import hubs_devices_sensors.serializers as serializers
from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.forms.models import model_to_dict
import django.core.exceptions as django_exceptions


class SensorListCreateAPIView(generics.ListCreateAPIView):

    """
    Class Based View for CREATE and LIST serialized Sensor objects
    @param permission_classes - permission classes for this Class Based View
    
    ALLOWED_METHODS: GET, POST
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(
            sensor_device__device_hub__owner=user
        )

    
class SensorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    """
    Class Based View SensorRetrieveUpdateDestroyAPIView
    Allows to Retrieve Update and Destroy single Sensor object
    @param permission_classes - permission classes for this Class Based View

    ALLOWED METHODS - GET, PUT, PATCH, DELETE
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorModelSerializer

    def get_queryset(self):
        user = self.request.user
        sensor = Sensor.objects.filter(pk=self.kwargs['pk'])

        try:
            if sensor.first().sensor_device.device_hub.owner == user:
                return sensor
            else:
                raise exceptions.PermissionDenied('You are not allowed to perform this action')
        except AttributeError:
            raise exceptions.NotFound('Requested Sensor was not found at our own')


class DeviceListCreateAPIView(generics.ListCreateAPIView):

    """
    Class Based View for CREATE and LIST serialized Device objects
    @param permission_classes - permission classes for this Class Based View
    
    ALLOWED_METHODS: GET, POST
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DeviceModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(device_hub__owner=user)


class DeviceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    """
    Class Based View DeviceRetrieveUpdateDestroy
    Allows to Retrieve Update and Destroy single Device object
    @param permission_classes - permission classes for this Class Based View

    ALLOWED METHODS - GET, PUT, PATCH, DELETE
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DeviceModelSerializer

    def get_queryset(self):
        user = self.request.user
        device = Device.objects.filter(pk=self.kwargs['pk'])
        try:
            if device.first().device_hub.owner == user:
                return device
            else:
                raise exceptions.PermissionDenied(
                    'You are not allowed to perform this action'
                )
        except AttributeError:
            raise exceptions.NotFound('Requested Device was not found at our own')


class DeviceListSensorsAPIView(generics.ListAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorModelSerializer

    def get_queryset(self):
        return Sensor.objects.filter(
            sensor_device=Device.objects.get(pk=self.kwargs['pk'])
        )


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

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.HubModelSerializer

    def get_queryset(self):
        return Device.objects.filter(
            device_hub=Hub.objects.get(pk=self.kwargs['pk'])
        )


class SensorCollectedDataListCreateAPIView(APIView):

    """
    Class Based View for LIST-CREATE serialized SensorCollectedData objects
    ALLOWED_METHODS: POST
    """

    def post(self, request, format=None):
        serializer = serializers.SensorCollectedDataModelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorCollectedDataAdminAPIView(generics.ListAPIView):

    """
    Class Based View for LIST all serialized SensorCollectedData objects
    Allowed only for Admin Users
    ALLOWED_METHODS: GET
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = SensorCollectedData.objects.all()
    serializer_class = serializers.SensorCollectedDataModelSerializer


class SensorAllCollectedDataUserAPIView(generics.ListAPIView):

    """
    Class Based View for LIST serialized SensorCollectedData objects
    related to current user
    Allowed only for Authenticated Users
    ALLOWED_METHODS: GET
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SensorCollectedDataModelSerializer

    def get_queryset(self):
        user = self.request.user
        return SensorCollectedData.objects.filter(
            sensor__sensor_device__device_hub__owner=user
        )


class OneSensorCollectedDataUserAPIView(generics.ListAPIView):

    """
    Class Based View for RETRIEVE serialized SensorCollectedData objects for  one related Sensor by current user
    Allowed only for Authenticated Users
    ALLOWED_METHODS: GET
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorCollectedDataModelSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            current_sensor = Sensor.objects.get(pk=self.kwargs['pk'])
            if current_sensor.sensor_device.device_hub.owner == user:
                return SensorCollectedData.objects.filter(
                    sensor=current_sensor,
                    sensor__sensor_device__device_hub__owner=user
                )
            else:
                raise exceptions.PermissionDenied('You are not allowed to perform this action')
        except Sensor.DoesNotExist:
            raise exceptions.NotFound('Requested Sensor Data was not found at our own')
