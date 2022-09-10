from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase, APIClient
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from apps.match.models import Match, MatchSeatInfo
from apps.stadium.models import Stadium, Seat
from apps.team.models import Team

User = get_user_model()


class TestMatchCreateAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('match:api_create_match')

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

        self.stadium = Stadium.objects.create(name='Azadi')
        self.host_team = Team.objects.create(name='Esteghlal')
        self.guest_team = Team.objects.create(name='Piroozi')
        self.now = timezone.now()

    def test_create_match_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team.pk,
                'datetime': self.now,
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertDictEqual(
            response.json(),
            {
                'match_info': {
                    'stadium': self.stadium.name,
                    'host_team': self.host_team.name,
                    'guest_team': self.guest_team.name,
                    'date': self.now.strftime('%d %b %Y'),
                    'time': self.now.strftime('%H : %M'),
                }
            }
        )

    def test_create_match_POST_invalid_first(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)

    def test_create_match_POST_invalid_second(self):
        """
        This method checks if both teams are the same.
        """

        response = self.client.post(
            path=self.url,
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.host_team.pk,
                'datetime': self.now,
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 0)

    def test_create_match_POST_invalid_third(self):
        """
        This method checks if a match with this stadium and datetime
        already exists.
        """

        Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now
        )

        response = self.client.post(
            path=self.url,
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team.pk,
                'datetime': self.now,
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(Match.objects.count(), 1)

    def test_create_match_POST_invalid_fourth(self):
        """
        This method checks if user is not authorized.
        """

        response = self.client.post(
            path=self.url,
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team.pk,
                'datetime': self.now,
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(Match.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'detail': _('Authentication credentials were not provided.')},
        )


class TestMatchSeatInfoCreateAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('match:api_create_match_seat')

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

        self.stadium = Stadium.objects.create(
            name='Azadi',
        )
        self.stadium2 = Stadium.objects.create(
            name='Shiroodi',
        )
        self.host_team = Team.objects.create(
            name='Esteghlal',
        )
        self.guest_team = Team.objects.create(
            name='Piroozi',
        )

        self.now = timezone.now()
        self.match = Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now,
        )

        self.seat = Seat.objects.create(
            stadium=self.stadium,
            code='n256',
        )
        self.seat2 = Seat.objects.create(
            stadium=self.stadium2,
            code='n256',
        )

    def test_create_match_seat_info_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seat': self.seat.pk,
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(MatchSeatInfo.objects.count(), 1)
        self.assertDictEqual(
            response.json(),
            {
                'match_seat_info': {
                    'match': str(self.match),
                    'seat': str(self.seat),
                    'price': 45000,
                }
            }
        )

    def test_create_match_seat_info_POST_invalid_first(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)

    def test_create_match_seat_info_POST_invalid_second(self):
        """
        This method checks if seat is already defined for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=5000,
        )

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seat': self.seat.pk,
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 1)

    def test_create_match_seat_info_POST_invalid_third(self):
        """
        This method checks if selected seat, belongs to stadium or not.
        """

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seat': self.seat2.pk,
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)

    def test_create_match_seat_info_POST_invalid_fourth(self):
        """
        This method checks if user is not authorized.
        """

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seat': self.seat.pk,
                'price': 45000,

            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'detail': _('Authentication credentials were not provided.')},
        )


class TestListCreateMatchSeatInfoAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.url = reverse('match:api_create_list_match_seat')

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

        self.stadium = Stadium.objects.create(
            name='Azadi',
        )
        self.stadium2 = Stadium.objects.create(
            name='Shiroodi',
        )
        self.host_team = Team.objects.create(
            name='Esteghlal',
        )
        self.guest_team = Team.objects.create(
            name='Piroozi',
        )

        self.now = timezone.now()
        self.match = Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now,
        )

        self.seat = Seat.objects.create(
            stadium=self.stadium,
            code='n256',
        )
        self.seat2 = Seat.objects.create(
            stadium=self.stadium,
            code='n2567',
        )
        self.seat3 = Seat.objects.create(
            stadium=self.stadium,
            code='n258',
        )
        self.seat4 = Seat.objects.create(
            stadium=self.stadium2,
            code='n259',
        )

    def test_list_create_match_seat_info_POST_valid(self):

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seats': [1, 2, 3],
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(MatchSeatInfo.objects.count(), 3)

    def test_list_create_match_seat_info_POST_invalid_first(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.post(
            path=self.url,
            data={},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)

    def test_list_create_match_seat_info_POST_invalid_second(self):
        """
        This method checks if one of seats is already defined for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=5000,
        )

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seats': [1, 2, 3],
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 1)

    def test_create_match_seat_info_POST_invalid_third(self):
        """
        This method checks if all selected seats, belongs to stadium or not.
        """

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seats': [1, 2, 4],
                'price': 45000,

            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)

    def test_list_create_match_seat_info_POST_invalid_fourth(self):
        """
        This method checks if user is not authorized.
        """

        response = self.client.post(
            path=self.url,
            data={
                'match': self.match.pk,
                'seats': [1, 2, 3],
                'price': 45000,

            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(MatchSeatInfo.objects.count(), 0)
        self.assertDictEqual(
            response.json(),
            {'detail': _('Authentication credentials were not provided.')},
        )


class TestListUpdateMatchSeatInfoAPIView(APITestCase):

    def setUp(self):

        self.client = APIClient()

        email = 'test@test.com'
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

        self.stadium = Stadium.objects.create(
            name='Azadi',
        )
        self.stadium2 = Stadium.objects.create(
            name='Shiroodi',
        )
        self.host_team = Team.objects.create(
            name='Esteghlal',
        )
        self.guest_team = Team.objects.create(
            name='Piroozi',
        )

        self.now = timezone.now()
        self.match = Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now,
        )
        self.url = reverse(
            'match:api_update_list_match_seat',
            kwargs={'match_id': self.match.pk},
        )

        self.seat = Seat.objects.create(
            stadium=self.stadium,
            code='n256',
        )
        self.seat2 = Seat.objects.create(
            stadium=self.stadium,
            code='n2567',
        )
        self.seat3 = Seat.objects.create(
            stadium=self.stadium,
            code='n258',
        )
        self.seat4 = Seat.objects.create(
            stadium=self.stadium2,
            code='n259',
        )

    def test_list_update_match_seat_info_POST_valid(self):

        response = self.client.put(
            path=self.url,
            data={
                'seats': [1, 2, 3],
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)

    def test_list_update_match_seat_info_POST_invalid_first(self):
        """
        This method checks if some parameters are missing.
        """

        response = self.client.put(
            path=self.url,
            data={},
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_list_update_match_seat_info_POST_invalid_second(self):
        """
        This method checks if one of seats is already reserved for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=5000,
            is_reserved=True,
        )

        response = self.client.put(
            path=self.url,
            data={
                'seats': [1, 2, 3],
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_update_match_seat_info_POST_invalid_third(self):
        """
        This method checks if all selected seats, belongs to stadium or not.
        """

        response = self.client.put(
            path=self.url,
            data={
                'seats': [1, 2, 4],
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_list_update_match_seat_info_POST_invalid_fourth(self):
        """
        This method checks if user is not authorized.
        """

        response = self.client.put(
            path=self.url,
            data={
                'seats': [1, 2, 3],
            },
            format='json',
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertDictEqual(
            response.json(),
            {'detail': _('Authentication credentials were not provided.')},
        )

    def test_list_update_match_seat_info_POST_invalid_fifth(self):
        """
        This method checks if match exist or not.
        """

        url = reverse(
            'match:api_update_list_match_seat',
            kwargs={'match_id': 12},
        )
        response = self.client.put(
            path=url,
            data={
                'seats': [1, 2, 3],
            },
            format='json',
            **self.headers,
        )

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
