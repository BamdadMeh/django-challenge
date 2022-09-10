from django.test import TestCase
from django.db import IntegrityError

from apps.stadium.models import Stadium, Seat


class TestStadiumModel(TestCase):

    def setUp(self):

        self.name = 'This is first stadium !!'
        self.slug = 'new-stadium-test'
        self.stadium = Stadium.objects.create(
            name=self.name,
            slug=self.slug,
        )

    def test_stadium_create(self):

        self.assertIsInstance(self.stadium, Stadium)
        self.assertEqual(self.stadium.name, self.name)
        self.assertEqual(self.stadium.slug, 'this-is-first-stadium')
        self.assertIsNone(self.stadium.save())

    def test_stadium_model_str_method(self):

        self.assertIsInstance(self.stadium.__str__(), str)
        self.assertEqual(self.stadium.__str__(), self.stadium.name)

    def test_stadium_model_save_method(self):

        self.assertIsNone(self.stadium.save())

    def test_stadium_instance_name_uniqueness(self):

        with self.assertRaises(IntegrityError):
            Stadium.objects.create(name=self.name)

    def test_stadium_instance_slug_uniqueness(self):

        with self.assertRaises(IntegrityError):
            Stadium.objects.create(name='This is first stadium #')


class TestSeatModel(TestCase):

    def setUp(self):

        self.stadium = Stadium.objects.create(name='This is first stadium')
        self.code = 'n256'
        self.seat = Seat.objects.create(stadium=self.stadium, code=self.code)

    def test_seat_create(self):

        self.assertIsInstance(self.seat, Seat)
        self.assertIsInstance(self.seat.stadium, Stadium)
        self.assertEqual(self.seat.stadium, self.stadium)
        self.assertEqual(self.seat.code, self.code)

    def test_seat_model_str_method(self):

        self.assertIsInstance(self.seat.__str__(), str)
        self.assertEqual(
            self.seat.__str__(),
            f'Code : {self.seat.code} - Stadium : {self.stadium.name}',
        )

    def test_unique_constraint_stadium_code(self):

        with self.assertRaises(IntegrityError):
            Seat.objects.create(stadium=self.stadium, code=self.code)
