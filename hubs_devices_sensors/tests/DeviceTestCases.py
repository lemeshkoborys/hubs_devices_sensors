from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from hubs_devices_sensors.models import Device, Hub, Sensor, SensorCollectedData
from hubs_devices_sensors.serializers import DeviceModelSerializer, SensorModelSerializer, SensorCollectedDataModelSerializer
import hubs_devices_sensors.tests.test_consts as CONSTS
import datetime

factory = APIRequestFactory()

class DeviceCanCreateAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber'
        )

    def test_device_can_create(self):
        device_data_to_create = {
            'device_title': 'My Device',
            'device_serial_number': 'DeviceSerialNum',
            'device_hub': self.hub.hub_serial_number
        }

        response = self.client.post(
            CONSTS.DEVICE_CREATE_URL,
            data=device_data_to_create,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(
            Device.objects.first().device_title,
            device_data_to_create['device_title']
        )


class DeviceCanGetListAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        Device.objects.create(
            device_title='Device #1',
            device_serial_number='Device1Serial',
            device_hub=self.hub
        )

        Device.objects.create(
            device_title='Device #2',
            device_serial_number='Device2Serial',
            device_hub=self.hub
        )

        Device.objects.create(
            device_title='Device #3',
            device_serial_number='Device3Serial',
            device_hub=self.hub
        )

    def test_device_can_get_list(self):
        response = self.client.get(CONSTS.DEVICE_LIST_URL)
        context = {
            'request': Request(factory.get(CONSTS.DEVICE_LIST_URL))
        }
        serialized_hubs = DeviceModelSerializer(
            Device.objects.all(),
            many=True,
            context=context
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_hubs.data)


class DeviceCanGetSingleAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        self.device = Device.objects.create(
            device_title='My Device',
            device_serial_number='MyDeviceSerial',
            device_hub=self.hub
        )

        self.url = '/api/tools/devices/' + str(self.device.id) + '/'
        self.request = Request(factory.get(self.url))

    def test_device_can_get_single(self):
        response = self.client.get(self.url)
        serialized_device = DeviceModelSerializer(
            self.device,
            context={
                'request': self.request
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_device.data)


class DeviceCanUpdateAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        self.device = Device.objects.create(
            device_title='My Device',
            device_serial_number='MyDeviceSerial',
            device_hub=self.hub
        )

        self.url = '/api/tools/devices/' + str(self.device.id) + '/update/'
        self.request = Request(factory.get(self.url))
    
    def test_device_can_put(self):
        data_to_put = {
            'device_title': 'Updated Title',
            'device_serial_number': 'UpdatedSerial',
            'device_hub': self.hub.hub_serial_number,
            'sensors_data_fetch_time': '00:05:00'
        }

        response = self.client.put(
            path=self.url,
            data=data_to_put,
            format='json'
        )

        serialized_device = DeviceModelSerializer(
            Device.objects.get(pk=self.device.id),
            context={'request': self.request}
        )
        self.assertEqual(
            Device.objects.get(pk=self.device.id).device_title,
            data_to_put['device_title']
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_device.data)
    
    def test_device_can_patch(self):
        data_to_patch = {
            'device_title': 'Patched title'
        }

        response = self.client.patch(
            path=self.url,
            data=data_to_patch,
            format='json'
        )

        serialized_device = DeviceModelSerializer(
            Device.objects.get(pk=self.device.id),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_device.data)
        self.assertEqual(
            Device.objects.get(pk=self.device.id).device_title,
            data_to_patch['device_title']
        )


class DeviceCanDeleteAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        self.device = Device.objects.create(
            device_title='My Device',
            device_serial_number='MyDeviceSerial',
            device_hub=self.hub
        )

        self.url = '/api/tools/devices/' + str(self.device.id) + '/delete/'
        self.request = Request(factory.get(self.url))

    def test_device_can_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DeviceGetSensorsAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        self.device = Device.objects.create(
            device_title='My Device',
            device_serial_number='MyDeviceSerial',
            device_hub=self.hub
        )

        Sensor.objects.create(
            sensor_title='Sensor 1',
            sensor_device=self.device,
            sensor_serial_number='sensor1serial',
            sensor_data_type='pH'
        )

        Sensor.objects.create(
            sensor_title='Sensor 2',
            sensor_device=self.device,
            sensor_serial_number='sensor2serial',
            sensor_data_type='CO2'
        )

        Sensor.objects.create(
            sensor_title='Sensor 3',
            sensor_device=self.device,
            sensor_serial_number='sensor3serial',
            sensor_data_type='Temperature'
        )

        self.url = '/api/tools/devices/' + str(self.device.id) + '/sensors/'
        self.request = Request(factory.get(self.url))

    def test_device_get_sensors(self):
        response = self.client.get(self.url)
        serialized_sensors = SensorModelSerializer(
            Sensor.objects.filter(sensor_device=self.device),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_sensors.data)


class DeviceGetCollectedDataTimeRangeAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'AdminStrongPassword'
        )

        self.client.login(
            username='admin',
            password='AdminStrongPassword'
        )

        self.hub = Hub.objects.create(
            hub_title='My Hub',
            hub_serial_number='HubSerialNumber',
            owner=self.superuser
        )

        self.device = Device.objects.create(
            device_title='My Device',
            device_serial_number='MyDeviceSerial',
            device_hub=self.hub
        )

        self.first_sensor = Sensor.objects.create(
            sensor_title='Sensor 1',
            sensor_device=self.device,
            sensor_serial_number='sensor1serial',
            sensor_data_type='pH'
        )

        self.second_sensor = Sensor.objects.create(
            sensor_title='Sensor 2',
            sensor_device=self.device,
            sensor_serial_number='sensor2serial',
            sensor_data_type='CO2'
        )

        self.third_sensor = Sensor.objects.create(
            sensor_title='Sensor 3',
            sensor_device=self.device,
            sensor_serial_number='sensor3serial',
            sensor_data_type='Temperature'
        )

        SensorCollectedData.objects.create(
            sensor=self.first_sensor,
            sensor_data_value=3.5,
            date_time_collected=datetime.datetime(2019, 2, 7, 8, 10, 22)
        )

        SensorCollectedData.objects.create(
            sensor=self.second_sensor,
            sensor_data_value=2.5,
            date_time_collected=datetime.datetime(2019, 2, 7, 10, 10, 32)
        )

        SensorCollectedData.objects.create(
            sensor=self.third_sensor,
            sensor_data_value=1.5,
            date_time_collected=datetime.datetime(2019, 2, 7, 15, 10, 32)
        )
        url_start = '/api/tools/devices/'
        url_end = '/sensors-collected-data/'
        url_params = '?start_datetime=2019-02-07T08:10:22Z&end_datetime=2019-02-07T15:10:32Z'
        self.url = url_start + str(self.device.id) + url_end + url_params
        self.request = Request(factory.get(self.url))

    def test_device_get_sensors_collected_data_time_range(self):
        response = self.client.get(self.url)

        serialized_collected_data = SensorCollectedDataModelSerializer(
            SensorCollectedData.objects.filter(sensor__sensor_device=self.device),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_collected_data.data)

    
    