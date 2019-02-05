"""
serializers.py
Classes:
    SensorCollectedDataModelSerializer,
    SensorModelSerializer,
    DeviceModelSerializer,
    HubModelSerializer
"""
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField
)
from index_app.serializers import UserBaseSerializer
from .models import Sensor, Device, Hub, SensorCollectedData


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


class SensorModelSerializer(HyperlinkedModelSerializer):

    """
    Class SensorModelSerializer - serializer for Sensor model
    Fields:
        'id',
        'sensor_title',
        'sensor_data_type',
        'sensor_device',
        'sensor_serial_number',
    """

    sensor_collected_data_url = HyperlinkedIdentityField(view_name='sensor-collected-data')

    class Meta:
        model = Sensor
        fields = (
            'id',
            'url',
            'sensor_title',
            'sensor_data_type',
            'sensor_device',
            'sensor_serial_number',
            'sensor_collected_data_url'
        )


class DeviceModelSerializer(HyperlinkedModelSerializer):

    """
    Class DeviceModelSerializer - serializer for Device model
    Fields:
        'id',
        'device_title',
        'device_serial_number',
        'device_hub'
    """

    device_sensors_url = HyperlinkedIdentityField(view_name='device-sensors')

    class Meta:
        model = Device
        fields = (
            'id',
            'url',
            'device_title',
            'device_serial_number',
            'device_hub',
            'device_sensors_url'
        )


class HubModelSerializer(HyperlinkedModelSerializer):

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

    devices_url = HyperlinkedIdentityField(view_name='hub-devices')

    owner = UserBaseSerializer(required=False)

    class Meta:
        model = Hub
        fields = (
            'id',
            'url',
            'hub_title',
            'hub_serial_number',
            'owner',
            'devices_url'
        )

# TODO Serilize timedelta