from django.urls import path

from apps.accounts.api_views import (

    UserCreateAPIView,
    UserLoginAPIView,
    UserTokenRefreshView,
    UserTokenVerifyView,
)


api_urls = [

    path('', UserCreateAPIView.as_view(), name='api_register'),
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path(
        'token_refresh/',
        UserTokenRefreshView.as_view(),
        name='api_token_refresh'
    ),
    path(
        'token_verify/',
        UserTokenVerifyView.as_view(),
        name='api_token_verify'
    ),
]
