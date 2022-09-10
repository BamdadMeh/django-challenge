from django.utils import timezone

from rest_framework.test import APITestCase

from apps.match.serializers import (
    MatchSerializer,
    MatchSeatInfoSerializer,
    ListCreateMatchSeatInfoSerializer,
    ListUpdateMatchSeatInfoSerializer,
)
from apps.match.models import Match, MatchSeatInfo
from apps.stadium.models import Seat, Stadium
from apps.team.models import Team


class TestMatchSerializer(APITestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(name='Azadi')
        self.host_team = Team.objects.create(name='Esteghlal')
        self.guest_team = Team.objects.create(name='Piroozi')
        self.now = timezone.now()

    def test_valid_data(self):

        srz_data = MatchSerializer(
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team.pk,
                'datetime': self.now,
            },
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if some parameters are missing.
        """

        srz_data = MatchSerializer(
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team.pk,
            },
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_second(self):
        """
        This method checks if both teams are the same.
        """

        srz_data = MatchSerializer(
            data={
                'stadium': self.stadium.pk,
                'host_team': self.guest_team.pk,
                'guest_team': self.guest_team.pk,
                'datetime': self.now,
            },
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if a match with this stadium and datetime
        already exists.
        """

        Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now,
        )

        srz_data = MatchSerializer(
            data={
                'stadium': self.stadium.pk,
                'host_team': self.host_team.pk,
                'guest_team': self.guest_team,
                'datetime': self.now,
            },
        )
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)


class TestMatchSeatInfoSerializer(APITestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(name='Azadi')
        self.host_team = Team.objects.create(name='Esteghlal')
        self.guest_team = Team.objects.create(name='Piroozi')

        self.now = timezone.now()
        self.match = Match.objects.create(
            stadium=self.stadium,
            host_team=self.host_team,
            guest_team=self.guest_team,
            datetime=self.now,
        )
        self.seat = Seat.objects.create(
            stadium=self.stadium,
            code='n400',
        )

    def test_valid_data(self):

        srz_data = MatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seat': self.seat.pk,
                'price': 4500,
            },
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if some parameters are missing.
        """

        srz_data = MatchSeatInfoSerializer(data={})

        self.assertFalse(srz_data.is_valid())

    def test_invalid_data_second(self):
        """
        This method checks if seat is already defined for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=6500,
        )

        srz_data = MatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seat': self.seat.pk,
                'price': 7500,
            },
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if selected seat, belongs to stadium or not.
        """

        srz_data = MatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seat': 12,
                'price': 8000,
            },
        )
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)


class TestListCreateMatchSeatInfoSerializer(APITestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(name='Azadi')
        self.stadium2 = Stadium.objects.create(name='Shiroodi')
        self.host_team = Team.objects.create(name='Esteghlal')
        self.guest_team = Team.objects.create(name='Piroozi')

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

    def test_valid_data(self):

        srz_data = ListCreateMatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seats': [1, 2, 3],
                'price': 45000,
            },
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if some parameters are missing.
        """

        srz_data = ListCreateMatchSeatInfoSerializer(data={})

        self.assertFalse(srz_data.is_valid())

    def test_invalid_data_second(self):
        """
        This method checks if one of seats is already defined for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=6500,
        )

        srz_data = ListCreateMatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seats': [1, 2, 3],
                'price': 45000,
            },
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if all selected seats, belongs to stadium or not.
        """

        srz_data = ListCreateMatchSeatInfoSerializer(
            data={
                'match': self.match.pk,
                'seats': [1, 2, 4],
                'price': 45000,
            },
        )
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)


class TestListUpdateMatchSeatInfoSerializer(APITestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(name='Azadi')
        self.stadium2 = Stadium.objects.create(name='Shiroodi')
        self.host_team = Team.objects.create(name='Esteghlal')
        self.guest_team = Team.objects.create(name='Piroozi')

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

    def test_valid_data(self):

        srz_data = ListUpdateMatchSeatInfoSerializer(
            data={
                'seats': [1, 2, 3],
            },
            match=self.match,
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if some parameters are missing.
        """

        srz_data = ListUpdateMatchSeatInfoSerializer(
            data={},
            match=self.match
        )

        self.assertFalse(srz_data.is_valid())

    def test_invalid_data_second(self):
        """
        This method checks if one of seats is already reserved for this match.
        """

        MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=6500,
            is_reserved=True,
        )

        srz_data = ListUpdateMatchSeatInfoSerializer(
            data={
                'seats': [1, 2, 3],
            },
            match=self.match,
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if all selected seats, belongs to stadium or not.
        """

        srz_data = ListUpdateMatchSeatInfoSerializer(
            data={
                'seats': [1, 2, 4],
            },
            match=self.match,
        )
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)
