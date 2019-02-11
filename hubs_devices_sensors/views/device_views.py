from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
import hubs_devices_sensors.serializers as serializers
from hubs_devices_sensors.models import Sensor, Device, Hub, SensorCollectedData


class DeviceListAPIView(generics.ListAPIView):

    """
    Class Based View for LIST serialized Device objects
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.DeviceModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(device_hub__owner=user)


class DeviceCreateAPIView(generics.CreateAPIView):

    """
    Class Based View for CREATE serialized Device objects
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

    """
    ClassBasedView that lists all Sensor entities related to Device
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorModelSerializer

    def get_queryset(self):
        return Sensor.objects.filter(
            sensor_device=Device.objects.get(pk=self.kwargs['pk'])
        )


class DeviceSensorsCollectedDataTimeRangeAPIView(generics.ListAPIView):

    """
    ClassBasedView taht lists all SensorCollectedData related to Device and filtered by time range
    e.g ?start_datetime=2018-01-02T21:25:33Z&end_datetime=2018-01-02T22:45:33Z
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorCollectedDataModelSerializer

    def get_queryset(self):
        start_datetime = self.request.query_params.get('start_datetime', None)
        end_datetime = self.request.query_params.get('end_datetime', None)
        user = self.request.user
        device = Device.objects.get(pk=self.kwargs['pk'])

        return SensorCollectedData.objects.filter(
            sensor__sensor_device__device_hub__owner=user,
            sensor__sensor_device=device,
            date_time_collected__range=(start_datetime, end_datetime)
        )
