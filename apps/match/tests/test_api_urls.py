from django.urls import reverse, resolve

from rest_framework.test import APISimpleTestCase

from apps.match.api_views import (
    MatchCreateAPIView,
    MatchSeatInfoCreateAPIView,
    ListCreateMatchSeatInfoAPIView,
    ListUpdateMatchSeatInfoAPIView,
)


class TestMatchAPIURLs(APISimpleTestCase):

    def test_create_match(self):

        url = reverse('match:api_create_match')
        self.assertEqual(
            resolve(url).func.view_class,
            MatchCreateAPIView,
        )

    def test_create_match_seat_info(self):

        url = reverse('match:api_create_match_seat')
        self.assertEqual(
            resolve(url).func.view_class,
            MatchSeatInfoCreateAPIView,
        )

    def test_list_create_match_seat_info(self):

        url = reverse('match:api_create_list_match_seat')
        self.assertEqual(
            resolve(url).func.view_class,
            ListCreateMatchSeatInfoAPIView,
        )

    def test_list_update_match_seat_info(self):

        url = reverse(
            'match:api_update_list_match_seat',
            kwargs={'match_id': 1}
        )
        self.assertEqual(
            resolve(url).func.view_class,
            ListUpdateMatchSeatInfoAPIView,
        )
