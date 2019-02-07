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

        self.hub = Hub.objects.create(
            hub_title='My 1 Hub',
            hub_serial_number='hub1serial',
            owner=self.superuser
        )

        self.url = '/api/tools/hubs/' + str(self.hub.id) + '/delete/'
        self.request = Request(factory.get(self.url))

    def test_can_delete(self):
        response = self.client.delete(
            self.url
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Hub.DoesNotExist):
            Hub.objects.get(pk=self.hub.id)


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
