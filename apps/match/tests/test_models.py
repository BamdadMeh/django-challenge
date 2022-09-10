from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from apps.match.models import Match, MatchSeatInfo
from apps.stadium.models import Stadium, Seat
from apps.team.models import Team


class TestMatchModel(TestCase):

    def setUp(self):

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

    def test_match_create(self):

        self.assertIsInstance(self.match, Match)
        self.assertIsInstance(self.match.stadium, Stadium)
        self.assertIsInstance(self.match.host_team, Team)
        self.assertIsInstance(self.match.guest_team, Team)
        self.assertIsInstance(self.match.datetime, datetime)
        self.assertEqual(self.match.datetime, self.now)

    def test_match_model_str_method(self):

        self.assertIsInstance(self.match.__str__(), str)
        self.assertEqual(
            self.match.__str__(),
            f'Host : {self.host_team.name}, Guest : {self.guest_team.name}'
        )

    def test_unique_constraint_stadium_datetime(self):

        with self.assertRaises(IntegrityError):
            Match.objects.create(
                stadium=self.stadium,
                host_team=self.host_team,
                guest_team=self.guest_team,
                datetime=self.now,
            )

    def test_match_model_clean_method(self):

        self.assertIsNone(self.match.clean())


class TestMatchSeatInfoModel(TestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(
            name='Azadi',
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

        self.price = 4500
        self.match_seat_info = MatchSeatInfo.objects.create(
            match=self.match,
            seat=self.seat,
            price=self.price,
        )

    def test_match_seat_info_create(self):

        self.assertIsInstance(self.match_seat_info, MatchSeatInfo)
        self.assertIsInstance(self.match_seat_info.match, Match)
        self.assertIsInstance(self.match_seat_info.seat, Seat)
        self.assertEqual(self.match_seat_info.price, self.price)
        self.assertIsNone(self.match_seat_info.buyer)
        self.assertFalse(self.match_seat_info.is_reserved)
        self.assertFalse(self.match_seat_info.is_paid)
        self.assertIsNone(self.match_seat_info.date_reserved)

    def test_match_model_str_method(self):

        self.assertIsInstance(self.match_seat_info.__str__(), str)
        self.assertEqual(
            self.match_seat_info.__str__(),
            f'Match : {self.match}, Code : {self.seat.code}'
        )

    def test_unique_constraint_match_seat(self):

        with self.assertRaises(IntegrityError):
            MatchSeatInfo.objects.create(
                match=self.match,
                seat=self.seat,
                price=self.price,
            )

    def test_match_seat_info_model_clean_method(self):

        self.assertIsNone(self.match_seat_info.clean())
