from django.test import TestCase
from django.db import IntegrityError

from apps.team.models import Team


class TestTeamModel(TestCase):

    def setUp(self):

        self.name = 'Esteghlal'
        self.team = Team.objects.create(name=self.name)

    def test_team_create(self):

        self.assertIsInstance(self.team, Team)
        self.assertEqual(self.team.name, self.name)

    def test_team_instance_name_uniqueness(self):

        with self.assertRaises(IntegrityError):
            Team.objects.create(name=self.name)

    def test_team_model_str_method(self):

        self.assertIsInstance(self.team.__str__(), str)
        self.assertEqual(self.team.__str__(), self.team.name)
