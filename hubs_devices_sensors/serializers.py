"""
serializers.py
Classes:
    SensorCollectedDataModelSerializer,
    SensorModelSerializer,
    DeviceModelSerializer,
    HubModelSerializer
"""
from rest_framework.serializers import ModelSerializer
from .models import Sensor, Device, Hub, SensorCollectedData
from index_app.serializers import UserBaseSerializer


class SensorCollectedDataModelSerializer(ModelSerializer):

    """
    Class SensorCollectedDataModelSerializer - serializer for SensorCollectedData model
    Fields:
        'id',
        'sensor',
        'date_time_collected',
        'sensor_data_value',
    """

    class Meta:
        model = SensorCollectedData
        fields = (
            'id',
            'sensor',
            'date_time_collected',
            'sensor_data_value',
        )


class SensorModelSerializer(ModelSerializer):

    """
    Class SensorModelSerializer - serializer for Sensor model
    Fields:
        'id',
        'sensor_title',
        'sensor_data_type',
        'sensor_device'
    """

    class Meta:
        model = Sensor
        fields = (
            'id',
            'sensor_title',
            'sensor_data_type',
            'sensor_device'
        )


class DeviceModelSerializer(ModelSerializer):

    """
    Class DeviceModelSerializer - serializer for Device model
    Fields:
        'id',
        'device_title',
        'device_serial_number',
        'device_hub'
    """

    class Meta:
        model = Device
        fields = (
            'id',
            'device_title',
            'device_serial_number',
            'device_hub'
        )


class HubModelSerializer(ModelSerializer):

    """
    Class HubModelSerializer - serializer for Hub model
    @param owner - Related object field of the UserBaseSerializer
    requierd=False kwarg setted for creation mathod. Owner relates automaticaly on create.
    Fields:
        'id',
        'hub_title',
        'hub_serial_number',
        'owner'
    """

    owner = UserBaseSerializer(required=False)

    class Meta:
        model = Hub
        fields = (
            'id',
            'hub_title',
            'hub_serial_number',
            'owner'
        )
