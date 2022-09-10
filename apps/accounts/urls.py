from django.urls import path, include

from apps.accounts.api_urls import api_urls


app_name = 'accounts'

urlpatterns = (
    path('api/', include(api_urls)),
)
