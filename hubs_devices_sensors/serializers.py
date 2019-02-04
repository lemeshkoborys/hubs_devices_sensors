from rest_framework.serializers import ModelSerializer
from .models import Sensor, Device, Hub, SensorCollectedData
from index_app.serializers import UserBaseSerializer


class SensorCollectedDataModelSerializer(ModelSerializer):

    class Meta:
        model = SensorCollectedData
        fields = (
            'id',
            'sensor',
            'date_time_collected',
            'sensor_data_value',
        )


class SensorModelSerializer(ModelSerializer):

    class Meta:
        model = Sensor
        fields = (
            'id',
            'sensor_title',
            'sensor_data_type',
            'sensor_device'
        )


class DeviceModelSerializer(ModelSerializer):

    class Meta:
        model = Device
        fields = (
            'id',
            'device_title',
            'device_serial_number',
            'device_hub'
        )


class HubModelSerializer(ModelSerializer):

    owner = UserBaseSerializer(required=False)

    class Meta:
        model = Hub
        fields = (
            'id',
            'hub_title',
            'hub_serial_number',
            'owner'
        )
