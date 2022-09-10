from django.urls import path, include

from apps.match.api_urls import api_urls


app_name = 'match'

urlpatterns = (
    path('api/', include(api_urls)),
)
