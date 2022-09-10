from django.urls import path, include

from apps.stadium.api_urls import api_urls


app_name = 'stadium'

urlpatterns = (
    path('api/', include(api_urls)),
)
