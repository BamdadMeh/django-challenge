from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from apps.stadium.models import Stadium
from apps.stadium.serializers import StadiumSerializer

User = get_user_model()


class TestStadiumSerializer(APITestCase):

    def test_valid_data(self):

        srz_data = StadiumSerializer(
            data={
                'name': 'ABC',
            }
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if parameter name is missing.
        """

        srz_data = StadiumSerializer(data={})

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_second(self):
        """
        This method checks if the sent value has incorrect type.
        """

        srz_data = StadiumSerializer(
            data={
                'name': ['Arman'],
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if a stadium with given name , already exists.
        """

        name = 'ABC'
        Stadium.objects.create(name=name)

        srz_data = StadiumSerializer(
            data={
                'name': name,
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)
