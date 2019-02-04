"""
models.py
Clases: Hub, Device, Sensor, SensorCollectedData
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import hubs_devices_sensors.sensor_consts as sensor_consts


class SensorCollectedData(models.Model):

    """
    Class SensorCollectedData - stores all collected data from sensors at current time
    @param date_time_collected - models.DateTimeField stores date and time data collected
    @param sensor -  models.ForeignKey('hubs_devices_sensors.Sensor') stores the foreign key
    to sensor which data is collected
    @param sensor_data_value - models.FloatField stores sensor value at current time

    @method clean() - performs validation of the sensor_data_value 
    @method save() - saves object after parforming clean() method
    """

    class Meta:
        db_table = 'sensor_collected_data'
        verbose_name = 'Sensor Collected Data'
        verbose_name_plural = 'Sensor Collected Data'

    date_time_collected = models.DateTimeField()

    sensor = models.ForeignKey(
        'hubs_devices_sensors.Sensor',
        on_delete=models.CASCADE,
        related_name='sensor_collected_data'
    )

    sensor_data_value = models.FloatField(
        blank=True,
        default=0.1
    )

    def clean(self, *args, **kwargs):
        if self.sensor.sensor_data_type == sensor_consts.PH_SENSOR:
            if self.sensor_data_value:
                if self.sensor_data_value > sensor_consts.PH_SENSOR_MAX_VALUE:
                    raise ValidationError('pH Value cannot be more than 14')
                elif self.sensor_data_value < sensor_consts.PH_SENSOR_MIN_VALIE:
                    raise ValidationError('pH Value cannot be less than 0')

        elif self.sensor.sensor_data_type == sensor_consts.CO2_SENSOR and self.sensor_data_value:
            if self.sensor_data_value:
                if self.sensor_data_value > sensor_consts.CO2_SENSOR_MAX_VALUE:
                    raise ValidationError('CO2 Value cannot be more than 100')
                elif self.sensor_data_value < sensor_consts.CO2_SENSOR_MIN_VALUE:
                    raise ValidationError('CO2 Value cannot be less than 0')

        elif self.sensor.sensor_data_type == sensor_consts.TEMPERATURE_SENSOR and self.sensor_data_value:
            if self.sensor_data_value:
                if self.sensor_data_value > sensor_consts.TEMPERATURE_SENSOR_MAX_VALUE:
                    raise ValidationError('CO2 Value cannot be more than 127')
                elif self.sensor_data_value < sensor_consts.TEMPERATURE_SENSOR_MIN_VALUE:
                    raise ValidationError('CO2 Value cannot be less than -40')

        else:
            raise ValidationError('No sensor data type was given')
        super(SensorCollectedData, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(SensorCollectedData, self).save(*args, **kwargs)


class Sensor(models.Model):

    """
    Class Sensor - stores data/information about current sensor
    @param SENSOR_DATA_TYPES - Enum that contains three types of sensor data type ('pH', 'CO2', 'Temperature')
    @param sensor_title - models.CharField(max_length=120) title/name of the current sensor
    @param sensor_device - sensor_device = models.ForeignKey('hubs_devices_sensors.Device') stores the foreign key
    to the related Device object
    @param sensor_data_type - models.CharField(max_length=30) stores Sensor data type (takes it from SENSOR_DATA_TYPE Enum)

    @method __str__(self) - string method. Returns Sensor title
    """

    SENSOR_DATA_TYPES = (
        (sensor_consts.PH_SENSOR, 'pH'),
        (sensor_consts.CO2_SENSOR, 'CO2'),
        (sensor_consts.TEMPERATURE_SENSOR, 'Temperature'),
    )

    class Meta:
        db_table = 'sensors'
        unique_together = (
            'sensor_device',
            'sensor_data_type'
        )

    sensor_title = models.CharField(max_length=120)

    sensor_device = models.ForeignKey(
        'hubs_devices_sensors.Device',
        on_delete=models.CASCADE,
        to_field='device_serial_number',
        related_name='sensors'
    )

    sensor_data_type = models.CharField(
        max_length=30,
        choices=SENSOR_DATA_TYPES
    )

    def __str__(self):
        return 'Sensor: ' + self.sensor_title + ' of Device: ' + str(self.sensor_device.device_title)



class Device(models.Model):

    """
    Class Device - Stores the data/information about Device
    @param device_title - models.CharField(max_length=120) stores device title/name
    @papram device hub - models.ForeignKey('hubs_devices_sensors.Hub') stores the foreign key to the related 
    Hub object
    @param device_serial_number - device_serial_number = models.CharField(max_length=16, unique=True) 
    unique field that stores Device serial number

    @method __str__(self) - string method. Returns Device title
    """

    class Meta:
        db_table = 'devices'

    device_title = models.CharField(max_length=120)

    device_hub = models.ForeignKey(
        'hubs_devices_sensors.Hub',
        on_delete=models.CASCADE,
        to_field='hub_serial_number',
        related_name='devices'
    )

    device_serial_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.device_title


class Hub(models.Model):

    """
    Class Device - Stores the data/information about Device
    @param hub_title - models.CharField(max_length=120) stores Hub title/name
    @param owner - models.ForeignKey(User) stores the foreign key to the related User object
    @param hub_serial_number - models.CharField(max_length=16, unique=True) unique field that stores Hub serial number

    @method __str__(self) - string method. Returns Hub title
    """

    class Meta:
        db_table = 'hubs'

    hub_title = models.CharField(max_length=120)
    
    hub_serial_number = models.CharField(max_length=16, unique=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.hub_title    
