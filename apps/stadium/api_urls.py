from django.urls import path

from apps.stadium.api_views import StadiumCreateAPIView


api_urls = [

    path('', StadiumCreateAPIView.as_view(), name='api_create_stadium'),

]
