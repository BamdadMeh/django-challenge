from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

User = get_user_model()


class TestUserCreateAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('accounts:api_register')

        email = 'A@test.com'
        password = 'admin12345QQ!!'
        user = User.objects.create_user(
            email=email,
            password=password,
        )

        api_login_url = reverse('accounts:api_login')

        response = self.client.post(
            api_login_url,
            data={
                'email': user.email,
                'password': password,
            },
            format='json',
        )
        access_token = response.json().get('access')
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}

    def test_create_user_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'email': 'test@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!Q',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertDictEqual(
            response.json(),
            {'email': 'test@test.com'},
        )

    def test_create_user_POST_invalid_first(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_POST_invalid_second(self):
        """
        This method checks if a user with given email , already exists.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': 'A@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!Q',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertNotEqual(User.objects.count(), 2)

    def test_create_user_POST_invalid_third(self):
        """
        This method checks if user is authenticated.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': 'test@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!Q',
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)
        self.assertDictEqual(
            response.json(),
            {'detail': _('You do not have permission to perform this action.')}
        )

    def test_create_user_POST_invalid_fourth(self):
        """
        This method checks if password and confirm_password are not equal.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': 'testQ@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!QVV',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertNotEqual(User.objects.count(), 2)


class TestUserLoginAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('accounts:api_login')
        self.password = 'admin12345QQ!!'
        self.user = User.objects.create_user(
            email='A@test.com',
            password=self.password,
        )

        response = self.client.post(
            self.url,
            data={
                'email': self.user.email,
                'password': self.password,
            },
            format='json',
        )
        access_token = response.json().get('access')
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}

    def test_login_user_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'email': self.user.email,
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())

    def test_login_user_POST_invalid_first(self):
        """
        This method checks if email or password is incorrect.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': 'Wow@test.com',
                'password': 'admin12345!Q',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertNotIn('accesss', response.json())
        self.assertNotIn('refresh', response.json())

    def test_login_user_POST_invalid_second(self):
        """
        This method checks if user is authenticated.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': self.user.email,
                'password': self.password,
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertDictEqual(
            response.json(),
            {'detail': _('You do not have permission to perform this action.')}
        )

    def test_login_user_POST_invalid_third(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.post(
            path=self.url,
            data={
                'email': self.user.email,
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class TestUserTokenRefreshView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('accounts:api_token_refresh')

        password = 'admin12345QQ!!'
        user = User.objects.create_user(
            email='A@test.com',
            password=password,
        )

        api_login_url = reverse('accounts:api_login')

        response = self.client.post(
            api_login_url,
            data={
                'email': user.email,
                'password': password,
            },
            format='json',
        )
        self.refresh_token = response.json().get('refresh')

    def test_user_token_refresh_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'refresh': self.refresh_token,
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', response.json())

    def test_user_token_refresh_POST_invalid_first(self):
        """
        This method checks if refresh parameter is missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_user_token_refresh_POST_invalid_second(self):
        """
        This method checks if refresh token is invalid or expired.
        """

        response = self.client.post(
            path=self.url,
            data={
                'refresh': 'abcd.qwer.zxcv',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertNotIn('accesss', response.json())


class TestUserTokenVerifyView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('accounts:api_token_verify')

        password = 'admin12345QQ!!'
        user = User.objects.create_user(
            email='A@test.com',
            password=password,
        )

        api_login_url = reverse('accounts:api_login')

        response = self.client.post(
            api_login_url,
            data={
                'email': user.email,
                'password': password,
            },
            format='json',
        )
        self.access_token = response.json().get('access')

    def test_user_token_verify_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'token': self.access_token,
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_token_verify_POST_invalid_first(self):
        """
        This method checks if token parameter is missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_user_token_verify_POST_invalid_second(self):
        """
        This method checks if token is invalid or expired.
        """

        response = self.client.post(
            path=self.url,
            data={
                'token': 'abcd.qwer.zxcv',
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
