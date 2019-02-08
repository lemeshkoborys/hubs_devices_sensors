# from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from hubs_devices_sensors.models import Hub
from hubs_devices_sensors.serializers import HubModelSerializer
import hubs_devices_sensors.tests.test_consts as CONSTS
import datetime

factory = APIRequestFactory()


class HubCanCreateAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
        self.client.login(
            username='admin',
            password='StrongPassword123'
        )
        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
        )

    def test_hub_create(self):
        data = {
            'hub_title': 'My Hub',
            'hub_serial_number': 'HDHDBV73634BDJ22'
        }
        response = self.client.post(
            CONSTS.HUB_CREATE_URL,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hub.objects.count(), 1)
        self.assertEqual(Hub.objects.get().hub_title, 'My Hub')
        self.assertEqual(Hub.objects.get().owner, self.superuser)

    def test_hub_create_not_authorized(self):
        self.client.logout()
        data = {
            'hub_title': 'My Hub',
            'hub_serial_number': 'HDHDBV73634BDJ22'
        }
        response = self.client.post(
            CONSTS.HUB_CREATE_URL,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_create_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        data = {
            'hub_title': 'My Hub',
            'hub_serial_number': 'HDHDBV73634BDJ22'
        }
        response = self.client.post(
            CONSTS.HUB_CREATE_URL,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_create_bad_request(self):
        data = {
            'hub_title': '',
            'hub_serial_number': 12344
        }
        response = self.client.post(
            CONSTS.HUB_CREATE_URL,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HubCanGetListAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
        self.client.login(
            username='admin',
            password='StrongPassword123'
        )

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
        )

        Hub.objects.create(
            hub_title='My 1 Hub',
            hub_serial_number='hub1serial',
            owner=self.superuser
        )

        Hub.objects.create(
            hub_title='My 2 Hub',
            hub_serial_number='hub2serial',
            owner=self.superuser
        )

        Hub.objects.create(
            hub_title='My 3 Hub',
            hub_serial_number='hub3serial',
            owner=self.superuser
        )

    def test_hub_get_list(self):
        response = self.client.get(CONSTS.HUB_LIST_URL)
        request = Request(factory.get(CONSTS.HUB_LIST_URL))
        serialized_hubs = HubModelSerializer(
            Hub.objects.all(),
            many=True,
            context={
                'request': request
            }
        )
        self.assertEqual(response.data, serialized_hubs.data)

    def test_hub_get_list_not_authorized(self):
        self.client.logout()
        response = self.client.get(CONSTS.HUB_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HubCanUpdateAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
        self.client.login(
            username='admin',
            password='StrongPassword123'
        )

        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
        )

        self.hub = Hub.objects.create(
            hub_title='My 1 Hub',
            hub_serial_number='hub1serial',
            owner=self.superuser
        )

        self.url = '/api/tools/hubs/' + str(self.hub.id) + '/update/'
        self.request = Request(factory.get(self.url))

    def test_hub_can_put(self):

        data_to_update = {
            'hub_title': 'My updated Hub',
            'hub_serial_number': 'hubserialupdated',
            'devices_data_fetch_time': '00:05:00',
            'hub_data_update_time': '00:10:00',
        }

        response = self.client.put(
            self.url,
            data=data_to_update,
            format='json'
        )

        serialized_hub = HubModelSerializer(
            Hub.objects.get(pk=self.hub.id),
            context={
                'request': self.request
            }
        )
        self.assertEqual(response.data, serialized_hub.data)

    def test_hub_can_patch(self):
        data_to_update = {
            'hub_data_update_time': '00:05:00'
        }

        response = self.client.patch(
            self.url,
            data=data_to_update,
            format='json'
        )

        serialized_hub = HubModelSerializer(
            Hub.objects.get(pk=self.hub.id),
            context={
                'request': self.request
            }
        )
        self.assertEqual(response.data, serialized_hub.data)

    def test_hub_update_not_authorized(self):
        self.client.logout()
        data_to_update = {
            'hub_title': 'My updated Hub',
            'hub_serial_number': 'hubserialupdated',
            'devices_data_fetch_time': '00:05:00',
            'hub_data_update_time': '00:10:00',
        }

        put_response = self.client.put(
            self.url,
            data=data_to_update,
            format='json'
        )

        patch_response = self.client.patch(
            self.url,
            data=data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_update_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        data_to_update = {
            'hub_title': 'My updated Hub',
            'hub_serial_number': 'hubserialupdated',
            'devices_data_fetch_time': '00:05:00',
            'hub_data_update_time': '00:10:00',
        }

        put_response = self.client.put(
            self.url,
            data=data_to_update,
            format='json'
        )

        patch_response = self.client.patch(
            self.url,
            data=data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_update_bad_request(self):
        invalid_data_to_update = {
            'hub_title': '',
            'hub_serial_number': 123222,
            'devices_data_fetch_time': 'HelloWorld',
            'hub_data_update_time': True,
        }

        put_response = self.client.put(
            self.url,
            data=invalid_data_to_update,
            format='json'
        )

        patch_response = self.client.patch(
            self.url,
            data=invalid_data_to_update,
            format='json'
        )

        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_hub_update_not_found(self):
        self.url = '/api/tools/hubs/123332/update/'
        data_to_put = {
            'hub_title': 'My updated Hub',
            'hub_serial_number': 'hubserialupdated',
            'devices_data_fetch_time': '00:05:00',
            'hub_data_update_time': '00:10:00',
        }

        response = self.client.put(
            self.url,
            data=data_to_put,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HubCanDeleteAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
        self.client.login(
            username='admin',
            password='StrongPassword123'
        )
        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'password'
        )
        self.hub = Hub.objects.create(
            hub_title='My 1 Hub',
            hub_serial_number='hub1serial',
            owner=self.superuser
        )

        self.url = '/api/tools/hubs/' + str(self.hub.id) + '/delete/'
        self.request = Request(factory.get(self.url))

    def test_can_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Hub.DoesNotExist):
            Hub.objects.get(pk=self.hub.id)

    def test_hub_delete_not_authorized(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_delete_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_delete_not_found(self):
        self.url = '/api/tools/hubs/123123123/delete/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HubCanGetSingleAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
        self.client.login(
            username='admin',
            password='StrongPassword123'
        )
        self.invalid_user = User.objects.create_user(
            'user',
            'user@example.com',
            'passwordss'
        )

        self.hub = Hub.objects.create(
            hub_title='My 1 Hub',
            hub_serial_number='hub1serial',
            owner=self.superuser
        )

        self.url = '/api/tools/hubs/' + str(self.hub.id) + '/'
        self.request = Request(factory.get(self.url))

    def test_hub_can_get_single(self):
        response = self.client.get(self.url)

        serialized_hub = HubModelSerializer(
            Hub.objects.get(pk=self.hub.id),
            context={
                'request': self.request
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_hub.data)

    def test_hub_get_single_not_authorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_get_single_permission_denied(self):
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_get_single_not_found(self):
        self.url = '/api/tools/hubs/12312313/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
