from django.shortcuts import render
from .models import Sensor, Device, Hub, SensorCollectedData
import hubs_devices_sensors.serializers as serializers
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.forms.models import model_to_dict


class SensorListCreateAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):

        sensors = Sensor.objects.filter(
            sensor_device__device_hub__owner=request.user
        )

        serializer = serializers.SensorModelSerializer(
            sensors,
            many=True
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.SensorModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeviceListCreateAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        devices = Device.objects.filter(device_hub__hub__owner=request.user)
        serializer = serializers.DeviceModelSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.DeviceModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HubListAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        hubs = Hub.objects.filter(owner=request.user)
        serializer = serializers.HubModelSerializer(hubs, many=True)
        return Response(serializer.data)


class HubCreateAPIView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, )

    queryset = Hub.objects.all()
    serializer_class = serializers.HubModelSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SensorCollectedDataListCreateAPIView(APIView):

    def post(self, request, format=None):
        serializer = serializers.SensorCollectedDataModelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorCollectedDataAdminAPIView(generics.ListAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = SensorCollectedData.objects.all()
    serializer_class = serializers.SensorCollectedDataModelSerializer


class SensorCollectedDataUserAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        sensors_collected_data = SensorCollectedData.objects.filter(
            sensor__sensor_device__device_hub__owner=request.user
        )

        serializer = serializers.SensorCollectedDataModelSerializer(
            list(sensors_collected_data),
            many=True
        )
        return Response(serializer.data)
