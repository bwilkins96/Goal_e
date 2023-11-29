from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile, Goal

class ProfileModelsTests(TestCase):
    """Tests for Profile model class"""

    @classmethod
    def setUp(cls):
        cls.test_user = User.objects.create_user(username='test_user')
        cls.test_profile = Profile.objects.create(user=cls.test_user)

    def test_add_points(self):
        self.test_profile.add_points(-500)
        self.assertEqual(self.test_profile.points, 0)

        self.test_profile.add_points(1000)
        self.assertEqual(self.test_profile.points, 1000)

    def test_get_points_str(self):
        self.test_profile.points = 0
        self.assertEqual(self.test_profile.get_points_str(), '0')

        self.test_profile.points = 1000
        self.assertEqual(self.test_profile.get_points_str(), '1,000')

        self.test_profile.points = 1000000
        self.assertEqual(self.test_profile.get_points_str(), '1,000,000')

