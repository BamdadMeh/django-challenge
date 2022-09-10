from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from apps.stadium.models import Stadium

User = get_user_model()


class TestStadiumCreateAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('stadium:api_create_stadium')

        email = 'test@test.com'
        password = 'admin12345QQ!!'
        user = User.objects.create_user(
            email=email,
            password=password,
            is_staff=True,
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

    def test_create_stadium_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'name': 'ABC',
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Stadium.objects.count(), 1)
        self.assertDictEqual(
            response.json(),
            {'name': 'ABC', 'slug': 'abc'},
        )

    def test_create_stadium_POST_invalid_first(self):
        """
        This method checks if parameter name is missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Stadium.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'name': [_('This field is required.')]}
        )

    def test_create_stadium_POST_invalid_second(self):
        """
        This method checks if the sent value has incorrect type.
        """

        response = self.client.post(
            path=self.url,
            data={'name': ['Arman']},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Stadium.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'name': [_('Not a valid string.')]},
        )

    def test_create_stadium_POST_invalid_third(self):
        """
        This method checks if a stadium with given name , already exists.
        """

        name = 'ABC'
        Stadium.objects.create(name=name)

        response = self.client.post(
            path=self.url,
            data={'name': 'ABC'},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Stadium.objects.count(), 1)
        self.assertNotEqual(Stadium.objects.count(), 2)
        self.assertDictEqual(
            response.json(),
            {'name': ['stadium with this name already exists.']},
        )

    def test_create_stadium_POST_invalid_fourth(self):
        """
        This method checks if user is not authorized.
        """

        response = self.client.post(
            path=self.url,
            data={'name': 'QWE'},
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(Stadium.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'detail': _('Authentication credentials were not provided.')},
        )
