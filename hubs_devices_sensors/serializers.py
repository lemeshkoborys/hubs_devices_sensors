from rest_framework.serializers import ModelSerializer, CharField, ListSerializer
from .models import Sensor, Device, Hub, SensorCollectedData
from index_app.serializers import UserBaseSerializer


class SensorCollectedDataModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(SensorCollectedDataModelSerializer, self).__init__(many=many, *args, **kwargs)


    class Meta:
        model = SensorCollectedData
        fields = (
            'id',
            'sensor',
            'date_time_collected',
            'sensor_data_value',
        )


class SensorModelSerializer(ModelSerializer):

    sensor_collected_data = SensorCollectedDataModelSerializer(many=True)

    class Meta:
        model = Sensor
        fields = (
            'id',
            'sensor_title',
            'sensor_data_type',
            'sensor_device',
            'sensor_collected_data'
        )


class DeviceModelSerializer(ModelSerializer):

    sensors = SensorModelSerializer(many=True)

    class Meta:
        model = Device
        fields = (
            'id',
            'device_title',
            'device_serial_number',
            'device_hub',
            'sensors'
        )
        # depth = 2


class HubModelSerializer(ModelSerializer):

    owner = UserBaseSerializer()

    class Meta:
        model = Hub
        fields = (
            'id',
            'hub_title',
            'hub_serial_number',
            'owner'
        )


class HubCollectedDataModelsSerializer(ModelSerializer):

    devices = DeviceModelSerializer(many=True)

    class Meta:
        model= Hub
        fields = (
            'id',
            'hub_title',
            'devices'
        )
