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

    def test_device_create_not_authorized(self):
        self.client.logout()
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_create_bad_request(self):
        device_data_to_create = {
            'device_title': '',
            'device_serial_number': 12312222,
            'device_hub': True
        }

        response = self.client.post(
            CONSTS.DEVICE_CREATE_URL,
            data=device_data_to_create,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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

    def test_device_get_list_not_authorized(self):
        self.client.logout()
        response = self.client.get(CONSTS.DEVICE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
        self.invalid_url = '/api/tools/devices/1231231231/'
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

    def test_device_get_single_not_authorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_single_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_single_not_found(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
        self.invalid_url = '/api/tools/devices/333442/update/'
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

    def test_device_update_not_authorized(self):
        self.client.logout()
        data_to_update = {
            'device_title': 'Updated Title',
            'device_serial_number': 'UpdatedSerial',
            'device_hub': self.hub.hub_serial_number,
            'sensors_data_fetch_time': '00:05:00'
        }
        put_response = self.client.put(
            path=self.url,
            data=data_to_update,
            format='json'
        )
        patch_response = self.client.patch(
            path=self.url,
            data=data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_update_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        data_to_update = {
            'device_title': 'Updated Title',
            'device_serial_number': 'UpdatedSerial',
            'device_hub': self.hub.hub_serial_number,
            'sensors_data_fetch_time': '00:05:00'
        }
        put_response = self.client.put(
            path=self.url,
            data=data_to_update,
            format='json'
        )
        patch_response = self.client.patch(
            path=self.url,
            data=data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_update_not_found(self):
        data_to_update = {
            'device_title': 'Updated Title',
            'device_serial_number': 'UpdatedSerial',
            'device_hub': self.hub.hub_serial_number,
            'sensors_data_fetch_time': '00:05:00'
        }
        put_response = self.client.put(
            path=self.invalid_url,
            data=data_to_update,
            format='json'
        )
        patch_response = self.client.patch(
            path=self.invalid_url,
            data=data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_device_update_bad_request(self):
        invalid_data_to_update = {
            'device_title': '',
            'device_serial_number': 3333,
            'device_hub': 'heeeelooooo',
            'sensors_data_fetch_time': False
        }
        put_response = self.client.put(
            path=self.url,
            data=invalid_data_to_update,
            format='json'
        )
        patch_response = self.client.patch(
            path=self.url,
            data=invalid_data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)


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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
        self.invalid_url = '/api/tools/devices/12322/delete/'
        self.request = Request(factory.get(self.url))

    def test_device_can_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_device_delete_not_authorized(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_delete_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_delete_not_found(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
        self.invalid_url = '/api/tools/devices/123/sensors/'
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

    def test_device_get_sensors_not_authorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.username
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_not_found(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
        self.invalid_url = url_start + '123332' + url_end + url_params
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

    def test_device_get_sensors_collected_data_not_authorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_collected_data_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.username
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_collected_data_not_found(self):
        with self.assertRaises(Device.DoesNotExist):
            self.client.get(self.invalid_url)
