"""
Test cases for User entities
Available test cases:
    UserCanRegisterAPITestCase,
    UserCanLoginAPITestCase,
    UserCanLogoutAPITestCase,
    UserCanGetProfileAPITestCase,
    AdminUserListAllUsersAPITestCase
"""
import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from index_app.serializers import UserBaseSerializer, UserForAdminModelSerializer
import index_app.test_consts as CONSTS


class UserCanRegisterAPITestCase(APITestCase):

    """
    Test case that ensures that User entity could be registred
    """

    def setUp(self):
        """
        Method make core actions to proceed the test case
        """
        self.user_data = {
            'username': 'test_case_user',
            'first_name': 'Test',
            'last_name': 'Case',
            'email': 'test@case.user',
            'password': 'TestCaseUserPassword123',
            'password_confirm': 'TestCaseUserPassword123'
        }

        self.invalid_user_data = {
            'username': '',
            'first_name': True,
            'last_name': 12333,
            'email': False,
            'password': 1333,
            'password_confirm': 'hellllllooooo'
        }

    def test_user_can_register(self):
        """
        Test tath ensures that User entity could be registred
        """
        response = self.client.post(
            CONSTS.USER_REGISTER_URL,
            data=self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_case_user')

    def test_user_register_bad_request(self):
        """
        Test tath ensures that User entity could not be registred by bad request (invalid data)
        """
        response = self.client.post(
            CONSTS.USER_REGISTER_URL,
            data=self.invalid_user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCanLoginAPITestCase(APITestCase):

    """
    Test case that ensures that User can login
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

    def test_user_can_login(self):
        """
        Test that ensures that User can login
        """
        response = self.client.post(
            CONSTS.USER_LOGIN_URL,
            data={
                'login': 'admin',
                'password': 'StrongPassword123'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get().is_active)

    def test_user_login_bad_request(self):
        """
        Test that ensures that User cannot login by bad request (invalid data)
        """
        response = self.client.post(
            CONSTS.USER_LOGIN_URL,
            data={
                'login': 'bad_login',
                'password': 'StrongPassword123'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCanLogoutAPITestCase(APITestCase):

    """
    Test case that ensures taht User can Logout
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

    def test_user_can_logout(self):
        """
        Test that ensures that User can Logout
        """
        response = self.client.post(
            CONSTS.USER_LOGOUT_URL,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(User.objects.get().last_login, datetime.datetime.now())


class UserCanGetProfileAPITestCase(APITestCase):

    """
    Test case that ensures that User can retrieve own profile
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

    def test_user_can_get_profile(self):
        """
        Test that ensures that User can retrieve own profile
        """
        response = self.client.get(CONSTS.USER_PROFILE_URL)
        serialized_user = UserBaseSerializer(self.superuser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_user.data)

    def test_user_get_profile_not_authorized(self):
        """
        Test that ensures that unauthorized User cannot retrieve own profile
        """
        self.client.logout()
        response = self.client.get(CONSTS.USER_PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserListAllUsersAPITestCase(APITestCase):

    """
    Test case taht ensures that Admin User can retrieve all User entities as list
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
            'hello123'
        )

        User.objects.create_user(
            'user_1',
            'user@1.com'
            'user1password'
        )

        User.objects.create_user(
            'user_2',
            'user@2.com'
            'user2password'
        )

        User.objects.create_user(
            'user_3',
            'user@3.com'
            'user3password'
        )

        self.users = UserForAdminModelSerializer(User.objects.all(), many=True)

    def test_admin_user_list_all_users(self):
        """
        Test taht ensures that Admin User Can retrieve all User entities as list
        """
        response = self.client.get(CONSTS.USER_ADMIN_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.users.data)

    def test_admin_user_list_all_users_permission_denied(self):
        """
        Test taht ensures that not Admin User cannot retrieve all User entities as list
        """
        self.client.logout()
        self.client.login(
            username=self.invalid_user.username,
            password=self.invalid_user.password
        )
        response = self.client.get(CONSTS.USER_ADMIN_LIST)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
