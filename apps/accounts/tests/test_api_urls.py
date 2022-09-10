from django.urls import reverse, resolve

from rest_framework.test import APISimpleTestCase

from apps.accounts.api_views import (

    UserCreateAPIView,
    UserLoginAPIView,
    UserTokenRefreshView,
    UserTokenVerifyView,
)


class TestAccountsAPIURLs(APISimpleTestCase):

    def test_create_user(self):

        url = reverse('accounts:api_register')
        self.assertEqual(resolve(url).func.view_class, UserCreateAPIView)

    def test_login_user(self):

        url = reverse('accounts:api_login')
        self.assertEqual(resolve(url).func.view_class, UserLoginAPIView)

    def test_user_token_refresh(self):

        url = reverse('accounts:api_token_refresh')
        self.assertEqual(resolve(url).func.view_class, UserTokenRefreshView)

    def test_user_token_verify(self):

        url = reverse('accounts:api_token_verify')
        self.assertEqual(resolve(url).func.view_class, UserTokenVerifyView)
