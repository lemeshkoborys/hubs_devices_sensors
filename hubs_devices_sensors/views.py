from django.shortcuts import render
from .models import Sensor, Device, Hub, SensorCollectedData
import hubs_devices_sensors.serializers as serializers
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response


class SensorListAPIView(generics.ListAPIView):

    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorModelSerializer


class DeviceListAPIView(generics.ListAPIView):

    queryset = Device.objects.all()
    serializer_class = serializers.DeviceModelSerializer


class HubListAPIView(generics.ListAPIView):

    queryset = Hub.objects.all()
    serializer_class = serializers.HubModelSerializer


class SensorCollectedDataListCreateAPIView(APIView):

    def post(self, request, format=None):
        serializer = serializers.SensorCollectedDataModelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class SensorCollectedDataAPIView(generics.ListAPIView):
    queryset = SensorCollectedData.objects.all()
    serializer_class = serializers.SensorCollectedDataModelSerializer

class HubsCollectedDataListAPIView(generics.ListAPIView):

    queryset = Hub.objects.all()
    serializer_class = serializers.HubCollectedDataModelsSerializer