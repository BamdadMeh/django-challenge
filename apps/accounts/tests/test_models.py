from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@test.com',
            password='admin12345!Q',
        )
        self.user2 = User.objects.create_user(
            email='test2@test.com',
            password='admin12345!Q',
            is_staff=True,
        )
        self.user3 = User.objects.create_user(
            email='test3@test.com',
            password='admin12345!Q',
            is_staff=True,
            is_superuser=True,
        )

    def test_user_create(self):

        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user2.is_staff)
        self.assertTrue(self.user3.is_superuser)

    def test_user_model_clean_method(self):

        self.assertIsNone(self.user.clean())

    def test_user_instance_email_uniqueness(self):

        with self.assertRaises(IntegrityError):
            self.user = User.objects.create_user(
                email='test@test.com',
                password='admin12345!Qvvvvv',
            )
