"""
Test Cases for Device Entities
Available test cases:
    HubCanCreateAPITestCase,
    HubCanGetListAPITestCase,
    HubCanUpdateAPITestCase,
    HubCanDeleteAPITestCase,
    HubCanGetSingleAPITestCase,

"""
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth.models import User
from hubs_devices_sensors.models import Hub
from hubs_devices_sensors.serializers import HubModelSerializer
import hubs_devices_sensors.tests.test_consts as CONSTS

FACTORY = APIRequestFactory()


class HubCanCreateAPITestCase(APITestCase):
    """
    Test case chacks if Hub entities could be created
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        """
        Test that ensures that Hub entity could be created by authorized User
        """
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
        """
        Test that ensures that Hub entity could not be created by unauthorized User
        """
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
        """
        Test that ensures that Hub entity could not be created by other Users
        """
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
        """
        Test that ensures that Hub entity could not be created by bad request (invalid data)
        """
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

    """
    Test case chacks if the Hub entities could be retrieved as list
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        """
        Test that ensures that Hub entities could be retrieved as list by authorized User
        """
        response = self.client.get(CONSTS.HUB_LIST_URL)
        request = Request(FACTORY.get(CONSTS.HUB_LIST_URL))
        serialized_hubs = HubModelSerializer(
            Hub.objects.all(),
            many=True,
            context={
                'request': request
            }
        )
        self.assertEqual(response.data, serialized_hubs.data)

    def test_hub_get_list_not_authorized(self):
        """
        Test that ensures that Hub entities could not be retrieved as list by unauthorized User
        """
        self.client.logout()
        response = self.client.get(CONSTS.HUB_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HubCanUpdateAPITestCase(APITestCase):

    """
    Test case taht ensures tath Hub entity could be updated
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_hub_can_put(self):
        """
        Test tath ensures tath Hub entity could be updated by authorized User
        using PUT method
        """

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
        """
        Test tath ensures tath Hub entity could be partly updated
        by authorized User using PATCH method
        """
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
        """
        Test tath ensures tath Hub entity could not be updated or partly updated
        by unauthorized User using PUT or PATCH method
        """
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
        """
        Test tath ensures tath Hub entity could not be updated or partly updated
        by other Users using PUT or PATCH method
        """
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
        """
        Test tath ensures tath Hub entity could not be updated or partly updated
        by bad request (invalid data)
        """
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
        """
        Test that ensures that system would notify that Hub entity is not found
        """
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

    """
    Test case that ensures that Hub entity could be deleted
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_can_delete(self):
        """
        Test that ensures that Hub entity could be deleted by authorized User
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Hub.DoesNotExist):
            Hub.objects.get(pk=self.hub.id)

    def test_hub_delete_not_authorized(self):
        """
        Test that ensures that Hub entity could not be deleted by unauthorized User
        """
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_delete_permission_denied(self):
        """
        Test that ensures that Hub entity could no be deleted by other Users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_delete_not_found(self):
        """
        Test that ensures that system would notify that Hub entity is not found
        """
        self.url = '/api/tools/hubs/123123123/delete/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HubCanGetSingleAPITestCase(APITestCase):

    """
    Test case that ensures that Hub single entity could be retrieved
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
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
        self.request = Request(FACTORY.get(self.url))

    def test_hub_can_get_single(self):
        """
        Test that ensures that Hub single entity could be retrieved by authorized User
        """
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
        """
        Test that ensures that Hub single entity could not be retrieved by unauthorized User
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_get_single_permission_denied(self):
        """
        Test that ensures that Hub single entity could not be retrieved by other Users
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hub_get_single_not_found(self):
        """
        Test that ensures that system would notify that Hub entity is not found
        """
        self.url = '/api/tools/hubs/12312313/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
