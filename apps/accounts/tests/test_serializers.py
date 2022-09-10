from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from apps.accounts.serializers import UserSerializer

User = get_user_model()


class TestUserSerializer(APITestCase):

    def test_valid_data(self):

        srz_data = UserSerializer(
            data={
                'email': 'test@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!Q',
            }
        )

        self.assertTrue(srz_data.is_valid())

    def test_invalid_data_first(self):
        """
        This method checks if email is not sent.
        """

        srz_data = UserSerializer(
            data={
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!Q',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_second(self):
        """
        This method checks if password is not sent.
        """

        srz_data = UserSerializer(
            data={
                'email': 'test@test.com',
                'confirm_password': 'admin12345!Q',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_third(self):
        """
        This method checks if confirm_password is not sent.
        """

        srz_data = UserSerializer(
            data={
                'email': 'test@test.com',
                'password': 'admin12345!Q',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_fourth(self):
        """
        This method checks if password and confirm_password are not equal.
        """

        srz_data = UserSerializer(
            data={
                'email': 'test@test.com',
                'password': 'admin12345!Q',
                'confirm_password': 'admin12345!QQQ',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_invalid_data_fifth(self):
        """
        This method checks if password and confirm_password are not sent.
        """

        srz_data = UserSerializer(
            data={
                'email': 'test@test.com',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 2)

    def test_invalid_data_sixth(self):
        """
        This method checks if email and confirm_password are not sent.
        """

        srz_data = UserSerializer(
            data={
                'password': 'admin12345!Q',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 2)

    def test_invalid_data_seventh(self):
        """
        This method checks if email and password are not sent.
        """

        srz_data = UserSerializer(
            data={
                'confirm_password': 'admin12345!Q',
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 2)

    def test_invalid_data_eight(self):
        """
        This method checks if data is empty
        """

        srz_data = UserSerializer(data={})

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 3)

    def test_invalid_data_ninth(self):
        """
        This method checks if an account with given email , already exists.
        """

        email = 'test@test.com'
        password = 'admin12345QQ!!'
        User.objects.create_user(
            email=email,
            password=password,
        )

        srz_data = UserSerializer(
            data={
                'email': email,
                'password': password,
                'confirm_password': password,
            }
        )

        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)
