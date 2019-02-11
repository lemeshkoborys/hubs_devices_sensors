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
    HyperlinkedIdentityField,
    ValidationError
)
from index_app.serializers import UserBaseSerializer
from .models import Sensor, Device, Hub, SensorCollectedData
import hubs_devices_sensors.sensor_consts as CONSTS


class SensorCollectedDataModelSerializer(ModelSerializer):

    """
    Class SensorCollectedDataModelSerializer - serializer for SensorCollectedData model
    Fields:
        'id',
        'sensor',
        'date_time_collected',
        'sensor_data_value',
    """

    def validate(self, data):
        if data['sensor'].sensor_data_type == CONSTS.PH_SENSOR:
            if data['sensor_data_value']:
                if data['sensor_data_value'] > CONSTS.PH_SENSOR_MAX_VALUE :
                    raise ValidationError('pH Value cannot be more than 14')
                elif data['sensor_data_value'] < CONSTS.PH_SENSOR_MIN_VALIE:
                    raise ValidationError('pH Value cannot be less than 0')

        elif data['sensor'].sensor_data_type == CONSTS.CO2_SENSOR:
            if data['sensor_data_value']:
                if data['sensor_data_value'] > CONSTS.CO2_SENSOR_MAX_VALUE:
                    raise ValidationError('CO2 Value cannot be more than 100')
                elif data['sensor_data_value'] < CONSTS.CO2_SENSOR_MIN_VALUE:
                    raise ValidationError('CO2 Value cannot be less than 0')

        elif data['sensor'].sensor_data_type == CONSTS.TEMPERATURE_SENSOR:
            if data['sensor_data_value']:
                if data['sensor_data_value'] > CONSTS.TEMPERATURE_SENSOR_MAX_VALUE:
                    raise ValidationError('Temperature Value cannot be more than 127')
                elif data['sensor_data_value'] < CONSTS.TEMPERATURE_SENSOR_MIN_VALUE:
                    raise ValidationError('Temperature Value cannot be less than -40')

        else:
            raise ValidationError('No sensor data type was given')
        return data

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
            'device_sensors_url',
            'sensors_data_fetch_time'
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
            'devices_data_fetch_time',
            'hub_data_update_time',
            'devices_url'
        )
