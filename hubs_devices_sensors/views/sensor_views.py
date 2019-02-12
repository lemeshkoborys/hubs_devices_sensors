from rest_framework import generics, exceptions
from hubs_devices_sensors.models import Sensor
from rest_framework.permissions import IsAuthenticated
import hubs_devices_sensors.serializers as serializers


class SensorListAPIView(generics.ListAPIView):

    """
    Class Based View for LIST serialized Sensor objects
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SensorModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(
            sensor_device__device_hub__owner=user
        )


class SensorCreateAPIView(generics.CreateAPIView):
    """
    Class Based View for CREATE serialized Sensor objects
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SensorModelSerializer
    queryset = Sensor.objects.all()


class SensorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    """
    Class Based View SensorRetrieveUpdateDestroyAPIView
    Allows to Retrieve Update and Destroy single Sensor object
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
