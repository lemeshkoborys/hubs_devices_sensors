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
from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
import hubs_devices_sensors.serializers as serializers
from hubs_devices_sensors.models import Sensor, SensorCollectedData


class SensorCollectedDataListCreateAPIView(APIView):

    """
    Class Based View for LIST-CREATE serialized SensorCollectedData objects
    """

    permission_classes = (AllowAny, )

    def post(self, request, format=None):

        """
        Post method that creaetes SensorCollectedData entities by POST request
        """

        serializer = serializers.SensorCollectedDataModelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorCollectedDataAdminAPIView(generics.ListAPIView):

    """
    Class Based View for LIST all serialized SensorCollectedData objects
    """

    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = SensorCollectedData.objects.all()
    serializer_class = serializers.SensorCollectedDataModelSerializer


class SensorAllCollectedDataUserAPIView(generics.ListAPIView):

    """
    Class Based View for LIST serialized SensorCollectedData objects related to current user
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



