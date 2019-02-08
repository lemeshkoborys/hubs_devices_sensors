"""
Test Cases for Device Entities
Available test cases:
    DeviceCanCreateAPITestCase,
    DeviceCanGetListAPITestCase,
    DeviceCanGetSingleAPITestCase,
    DeviceCanUpdateAPITestCase,
    DeviceCanDeleteAPITestCase,
    DeviceGetSensorsAPITestCase,
    DeviceGetCollectedDataTimeRangeAPITestCase
"""
import datetime
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from hubs_devices_sensors.models import Device, Hub, Sensor, SensorCollectedData
from hubs_devices_sensors.serializers import (
    DeviceModelSerializer,
    SensorModelSerializer,
    SensorCollectedDataModelSerializer
)
import hubs_devices_sensors.tests.test_consts as CONSTS

FACTORY = APIRequestFactory()


class DeviceCanCreateAPITestCase(APITestCase):

    """
    Test case check if the Device entity could be creaeted
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        """
        Test that ensures that Device entity is being created
        """
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
        """
        Test that ensures that sensor could not be created without authentification
        """
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
        """
        Test that ensures that POST data could not be invalid
        """
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

    """
    Test case chack if Sensor entities could be getted as list
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        """
        Test that ensures that authenticated user can get own Device entities
        """
        response = self.client.get(CONSTS.DEVICE_LIST_URL)
        context = {
            'request': Request(FACTORY.get(CONSTS.DEVICE_LIST_URL))
        }
        serialized_hubs = DeviceModelSerializer(
            Device.objects.all(),
            many=True,
            context=context
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_hubs.data)

    def test_device_get_list_not_authorized(self):
        """
        Test that ensures that Device entities could not be retirieved without authentification
        """
        self.client.logout()
        response = self.client.get(CONSTS.DEVICE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeviceCanGetSingleAPITestCase(APITestCase):

    """
    Test case chack if Device single entity could be getted
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_device_can_get_single(self):
        """
        Test that ensures that authenticated user can get single Device entity
        """
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
        """
        Test that ensures that Device entities could not be retirieved without authentification
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_single_permission_denied(self):
        """
        Test that ensures that Device entity could not be retrieved by other users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_single_not_found(self):
        """
        Test that ensures that system would notify that Device entity is not found
        """
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceCanUpdateAPITestCase(APITestCase):

    """
    Test case checks that Device entity could be updated
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_device_can_put(self):
        """
        Test that ensures that Device entity could be updated by PUT method
        """
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
        """
        Test that ensures that Device entity could not be updated without authentification
        using PUT method
        """
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
        """
        Test that ensures that Sensor entity could not be partly updated without
        authentification using PATCH method
        """
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
        """
        Test that ensures that Device entity could not be updated or partly updated
        by other users using PUT or PATCH method
        """
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
        """
        Test that ensures that system would notify that Device entity is not found
        """
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
        """
        Test taht ensures that Device entity could not be updated by bad request (invalid data)
        """
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

    """
    Test case checks that Device entity could be deleted
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_device_can_delete(self):
        """
        Test that ensures that Device entity could be deleted by authorized user
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_device_delete_not_authorized(self):
        """
        Test that ensures that Device entity could not be deleted by unauthorized user
        """
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_delete_permission_denied(self):
        """
        Test that ensures that Device entity could not be deleted by other users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_delete_not_found(self):
        """
        Test that ensures that system would notify that Sensor entity is not found
        """
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceGetSensorsAPITestCase(APITestCase):

    """
    Test case checks if Sensor entities could be retrieved for certain Device entity
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_device_get_sensors(self):
        """
        Test that ensures that Sensor entities could be retrieved for certain Device
        """
        response = self.client.get(self.url)
        serialized_sensors = SensorModelSerializer(
            Sensor.objects.filter(sensor_device=self.device),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_sensors.data)

    def test_device_get_sensors_not_authorized(self):
        """
        Test that ensures that not authorized users cannot retrieve Sensor entities
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_permission_denied(self):
        """
        Test that ensures that other users cannot retrieve Sensor entities
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.username
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_not_found(self):
        """
        Test that ensures that system would notify that Device entity is not found
        """
        with self.assertRaises(Device.DoesNotExist):
            self.client.get(self.invalid_url)


class DeviceGetCollectedDataTimeRangeAPITestCase(APITestCase):

    """
    Test case checks if SensorCollectedData entities could be retrieved
    by certain User and time range
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_device_get_sensors_collected_data_time_range(self):
        """
        Test that ensures that SensorCollectedData entities could be retrieved
        by authorized Users and certain datetime range
        """
        response = self.client.get(self.url)

        serialized_collected_data = SensorCollectedDataModelSerializer(
            SensorCollectedData.objects.filter(sensor__sensor_device=self.device),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_collected_data.data)

    def test_device_get_sensors_collected_data_not_authorized(self):
        """
        Test that ensures that SensorCollectedData entities could not be retrieved
        by unauthorized Users and certain datetime range
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_collected_data_permission_denied(self):
        """
        Test that ensures that SensorCollectedData with certain datetime range entities
        could not be retrieved by other Users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.username
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_device_get_sensors_collected_data_not_found(self):
        """
        Test that ensures that system would notify that Device entity is not found
        """
        with self.assertRaises(Device.DoesNotExist):
            self.client.get(self.invalid_url)
