from django.urls import reverse, resolve

from rest_framework.test import APISimpleTestCase

from apps.stadium.api_views import StadiumCreateAPIView


class TestStadiumAPIURLs(APISimpleTestCase):

    def test_create_stadium(self):

        url = reverse('stadium:api_create_stadium')
        self.assertEqual(resolve(url).func.view_class, StadiumCreateAPIView)
