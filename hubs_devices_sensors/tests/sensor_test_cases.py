"""
Sensor Test Cases
Available test cases:
    SensorCanCreateAPITestCase,
    SensorCanGetAPITestCase,
    SensorCanUpdateAPITesCase,
    SensorCanDeleteAPITestCase,
    SensorCanCollectDataAPITestCase
"""
import datetime
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from hubs_devices_sensors.models import Device, Hub, Sensor, SensorCollectedData
from hubs_devices_sensors.serializers import (
    SensorModelSerializer,
    SensorCollectedDataModelSerializer
)

FACTORY = APIRequestFactory()


class SensorCanCreateAPITestCase(APITestCase):

    """
    Test case check if the Sensor entity could be creaeted
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

        self.device = Device.objects.create(
            device_title='Sensor parent Device',
            device_serial_number='XJHFJQWH6EASKAS2',
            device_hub=self.hub
        )

        self.url = '/api/tools/sensors/create/'
        self.request = Request(FACTORY.get(self.url))

    def test_sensor_can_create(self):
        """
        Test that ensures that sensor entity is being created
        """
        sensor_data_to_post = {
            'sensor_title': 'My pH Sensor',
            'sensor_serial_number': 'XJHFJQWH6EASSAS2',
            'sensor_data_type': 'pH',
            'sensor_device': self.device.device_serial_number
        }

        response = self.client.post(
            path=self.url,
            data=sensor_data_to_post,
            format='json'
        )

        serialized_sensor = SensorModelSerializer(
            Sensor.objects.get(),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serialized_sensor.data)

    def test_sensor_create_not_authenticated(self):
        """
        Test that ensures that sensor could not be created without authentification
        """
        self.client.logout()
        sensor_data_to_post = {
            'sensor_title': 'My pH Sensor',
            'sensor_serial_number': 'XJHFJQWH6EASSAS2',
            'sensor_data_type': 'pH',
            'sensor_device': self.device.device_serial_number
        }

        response = self.client.post(
            path=self.url,
            data=sensor_data_to_post,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_create_invalid_data(self):
        """
        Test that ensures that POST data could not be invalid
        """
        sensor_invalid_create_data = {
            'sensor_title': '',
            'sensor_serial_number': 'XJHFJQWH6EASSAS2awsdasd',
            'sensor_data_type': 'Bubble',
            'sensor_device': self.device.device_serial_number
        }

        response = self.client.post(
            path=self.url,
            data=sensor_invalid_create_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SensorCanGetAPITestCase(APITestCase):
    """
    Test case chack if Sensor entity could be getted
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

        self.device = Device.objects.create(
            device_title='Sensor parent Device',
            device_serial_number='XJHFJQWH6EASKAS2',
            device_hub=self.hub
        )

        self.sensor = Sensor.objects.create(
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

        self.list_url = '/api/tools/sensors/'
        self.single_url = '/api/tools/sensors/' + str(Sensor.objects.first().id) + '/'

    def test_sensor_get_list(self):
        """
        Test that ensures that authenticated user can get own Sensor entities
        """

        request = Request(FACTORY.get(self.list_url))
        response = self.client.get(self.list_url)

        serialized_sensors = SensorModelSerializer(
            Sensor.objects.all(),
            many=True,
            context={'request': request}
        )

        self.assertEqual(response.data, serialized_sensors.data)

    def test_sensor_get_single(self):
        """
        Test that ensures that authenticated user can get single Sensor entity
        """
        request = Request(FACTORY.get(self.single_url))
        response = self.client.get(self.single_url)

        serialized_sensor = SensorModelSerializer(
            Sensor.objects.first(),
            context={'request': request}
        )
        self.assertEqual(response.data, serialized_sensor.data)

    def test_sensor_get_collected_data(self):
        """
        Test that ensures that authenticated user can get own Sensor Collected Data entities
        """

        SensorCollectedData.objects.create(
            sensor=self.sensor,
            sensor_data_value=12,
            date_time_collected=datetime.datetime.now()
        )

        SensorCollectedData.objects.create(
            sensor=self.sensor,
            sensor_data_value=11,
            date_time_collected=datetime.datetime.now()
        )

        url = '/api/tools/sensors/' + str(self.sensor.id) + '/collected-data/'
        request = Request(FACTORY.get(url))

        response = self.client.get(url)

        serialized_sensor_data_collected = SensorCollectedDataModelSerializer(
            SensorCollectedData.objects.filter(sensor=self.sensor),
            many=True,
            context={'request': request}
        )

        self.assertEqual(response.data, serialized_sensor_data_collected.data)

    def test_get_sensors_not_authorized(self):
        """
        Test that ensures that Sensor entities could not be retirieved without authentification
        """
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_sensor_permission_denied(self):
        """
        Test that ensures that Sensor entity could not be retrieved by other users
        """
        self.client.logout()
        User.objects.create_user(
            'user',
            'user@example.com',
            'userPassword'
        )
        self.client.login(
            username='user',
            password='userPassword'
        )
        response = self.client.get(self.single_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_get_not_found(self):
        """
        Test that ensures that system would notify that Sensor entity is not found
        """
        self.single_url = '/api/tools/sensors/123/'
        response = self.client.get(self.single_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SensorCanUpdateAPITesCase(APITestCase):

    """
    Test case checks that Sensor entity could be updated
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

        self.device = Device.objects.create(
            device_title='Sensor parent Device',
            device_serial_number='XJHFJQWH6EASKAS2',
            device_hub=self.hub
        )

        self.sensor = Sensor.objects.create(
            sensor_title='Sensor 1',
            sensor_device=self.device,
            sensor_serial_number='sensor1serial',
            sensor_data_type='pH'
        )

        self.url = '/api/tools/sensors/' + str(self.sensor.id) + '/update/'
        self.request = Request(FACTORY.get(self.url))

    def test_sensor_can_put(self):
        """
        Test that ensures that Sensor entity could be updated by PUT method
        """
        sensor_data_to_put = {
            'sensor_title': 'Updated Title',
            'sensor_serial_number': 'updatedserial',
            'sensor_device': self.device.device_serial_number,
            'sensor_data_type': 'pH'
        }
        response = self.client.put(
            path=self.url,
            data=sensor_data_to_put,
            format='json'
        )

        serialized_sensor = SensorModelSerializer(
            Sensor.objects.get(pk=self.sensor.id),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_sensor.data)
        self.assertEqual(
            Sensor.objects.get(pk=self.sensor.id).sensor_title,
            sensor_data_to_put['sensor_title']
        )

    def test_sensor_can_patch(self):
        """
        Test ensures that Sensor entity could be partly updated by PATCH method
        """
        sensor_data_to_patch = {
            'sensor_title': 'Patched title'
        }

        response = self.client.patch(
            path=self.url,
            data=sensor_data_to_patch,
            format='json'
        )
        serialized_sensor = SensorModelSerializer(
            Sensor.objects.get(pk=self.sensor.id),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_sensor.data)
        self.assertEqual(
            Sensor.objects.get(pk=self.sensor.id).sensor_title,
            sensor_data_to_patch['sensor_title']
        )

    def test_sensor_put_not_authorized(self):
        """
        Test that ensures that Sensor entity could not be updated without authentification
        using PUT method
        """
        self.client.logout()
        sensor_data_to_put = {
            'sensor_title': 'Updated Title',
            'sensor_serial_number': 'updatedserial',
            'sensor_device': self.device.device_serial_number,
            'sensor_data_type': 'pH'
        }
        response = self.client.put(
            path=self.url,
            data=sensor_data_to_put,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_patch_not_authorized(self):
        """
        Test that ensures that Sensor entity could not be partly updated without
        authentification using PATCH method
        """
        self.client.logout()
        sensor_data_to_patch = {
            'sensor_title': 'Updated Title'
        }
        response = self.client.patch(
            path=self.url,
            data=sensor_data_to_patch,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_put_permission_denied(self):
        """
        Test that ensures that Sensor entity could not be updated by other users
        using PUT method
        """
        self.client.logout()
        User.objects.create_user(
            'user',
            'email@example.com',
            'password'
        )
        self.client.login(
            username='user',
            password='password'
        )

        sensor_data_to_put = {
            'sensor_title': 'Updated Title',
            'sensor_serial_number': 'updatedserial',
            'sensor_device': self.device.device_serial_number,
            'sensor_data_type': 'pH'
        }
        response = self.client.put(
            path=self.url,
            data=sensor_data_to_put,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_patch_permission_denied(self):
        """
        Test that ensures that Sensor entity could not be partly updated
        by other users using PATCH method
        """
        self.client.logout()
        User.objects.create_user(
            'user',
            'email@example.com',
            'password'
        )
        self.client.login(
            username='user',
            password='password'
        )

        sensor_data_to_patch = {
            'sensor_title': 'Updated Title',
        }
        response = self.client.patch(
            path=self.url,
            data=sensor_data_to_patch,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_update_bad_request(self):
        """
        Test taht ensures that Sensor entity could not be updated by bad request (invalid data)
        """
        sensor_invalid_update_data = {
            'sensor_title': ''
        }

        patch_response = self.client.patch(
            path=self.url,
            data=sensor_invalid_update_data,
            format='json'
        )
        put_response = self.client.put(
            path=self.url,
            data=sensor_invalid_update_data,
            format='json'
        )
        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sensor_update_not_found(self):
        """
        Test that ensures that system would notify that Sensor entity is not found
        """
        self.url = '/api/tools/sensors/123321/update/'
        sensor_data_to_update = {
            'sensor_title': 'Updated Title',
            'sensor_serial_number': 'updatedserial',
            'sensor_device': self.device.device_serial_number,
            'sensor_data_type': 'pH'
        }

        patch_response = self.client.patch(
            path=self.url,
            data=sensor_data_to_update,
            format='json'
        )
        put_response = self.client.put(
            path=self.url,
            data=sensor_data_to_update,
            format='json'
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)


class SensorCanDeleteAPITestCase(APITestCase):

    """
    Test case checks that Sensor entity could be deleted
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

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
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
            device_title='Sensor parent Device',
            device_serial_number='XJHFJQWH6EASKAS2',
            device_hub=self.hub
        )

        self.sensor = Sensor.objects.create(
            sensor_title='Sensor 1',
            sensor_device=self.device,
            sensor_serial_number='sensor1serial',
            sensor_data_type='pH'
        )

        self.url = '/api/tools/sensors/' + str(self.sensor.id) + '/delete/'
        self.request = Request(FACTORY.get(self.url))

    def test_sensor_can_delete(self):
        """
        Test that ensures that Sensor entity could be deleted by authorized user
        """
        response = self.client.delete(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_sensor_delete_not_authorized(self):
        """
        Test that ensures that Sensor entity could not be deleted by unauthorized user
        """
        self.client.logout()
        response = self.client.delete(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_delete_permission_denied(self):
        """
        Test that ensures that Sensor entity could not be deleted by other users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.delete(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sensor_delete_not_found(self):
        """
        Test that ensures that system would notify that Sensor entity is not found
        """
        self.url = '/api/tools/sensors/123332/delete/'
        response = self.client.delete(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SensorCanCollectDataAPITestCase(APITestCase):
    """
    Test case checks that SensorCollectedData enteties could be created
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

        self.device = Device.objects.create(
            device_title='Sensor parent Device',
            device_serial_number='XJHFJQWH6EASKAS2',
            device_hub=self.hub
        )

        self.sensor = Sensor.objects.create(
            sensor_title='Sensor 1',
            sensor_device=self.device,
            sensor_serial_number='sensor1serial',
            sensor_data_type='pH'
        )
        self.url = '/api/tools/sensors/collect-data/'
        self.request = Request(FACTORY.get(self.url))

    def sensor_can_collect_data(self):
        """
        Test ensures that SensorCollectedData entities could be created
        """
        sensor_data_to_collect = [
            {
                'sensor': self.sensor.sensor_serial_number,
                'sensor_data_value': 0.35,
                'date_time_collected': datetime.datetime.now()
            },
            {
                'sensor': self.sensor.sensor_serial_number,
                'sensor_data_value': 1.35,
                'date_time_collected': datetime.datetime.now()
            },
            {
                'sensor': self.sensor.sensor_serial_number,
                'sensor_data_value': 2.35,
                'date_time_collected': datetime.datetime.now()
            }
        ]

        response = self.client.post(
            path=self.url,
            data=sensor_data_to_collect,
            format='json'
        )

        serialized_sensor_collected_data = SensorCollectedDataModelSerializer(
            SensorCollectedData.objects.filter(sensor=self.sensor),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serialized_sensor_collected_data.data)

    def test_sensor_collect_data_bad_request(self):
        """
        Test that ensures that SensorCollectedData entities could not be created
        by bad request (invalid data)
        """

        sensor_data_to_collect = [
            {
                'sensor': 'asd',
                'sensor_data_value': 'asdddddddddd',
                'date_time_collected': 'hellllllllloooouuu'
            }
        ]

        response = self.client.post(
            path=self.url,
            data=sensor_data_to_collect,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
