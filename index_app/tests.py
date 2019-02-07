from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from index_app.serializers import UserBaseSerializer, UserForAdminModelSerializer
import index_app.test_consts as CONSTS
import datetime


class UserCanRegisterAPITestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'test_case_user',
            'first_name': 'Test',
            'last_name': 'Case',
            'email': 'test@case.user',
            'password': 'TestCaseUserPassword123',
            'password_confirm': 'TestCaseUserPassword123'
        }

    def test_user_can_register(self):
        response = self.client.post(
            CONSTS.USER_REGISTER_URL,
            data=self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_case_user')


class UserCanLoinAPITestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'StrongPassword123'
        )
    
    def test_user_can_login(self):
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


class UserCanLogoutAPITestCase(APITestCase):

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

    def test_user_can_logout(self):
        response = self.client.post(
            CONSTS.USER_LOGOUT_URL,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(User.objects.get().last_login, datetime.datetime.now())


class UserCanGetProfileAPITestCase(APITestCase):

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

    def test_user_can_get_profile(self):
        response = self.client.get(CONSTS.USER_PROFILE_URL)
        serialized_user = UserBaseSerializer(self.superuser)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_user.data)


class AdminUserListAllUsersAPITestCase(APITestCase):

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
        response = self.client.get(
            CONSTS.USER_ADMIN_LIST
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.users.data)
