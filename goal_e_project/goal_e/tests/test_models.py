from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile, Goal
from ..utils import get_week_from_today

class ProfileModelTests(TestCase):
    """Tests for Profile model class"""
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')
        cls.profile = Profile.objects.create(user=cls.user)

    def test_add_points(self):
        self.profile.add_points(-500)
        self.assertEqual(self.profile.points, 0)

        self.profile.add_points(1000)
        self.assertEqual(self.profile.points, 1000)

    def test_get_points_str(self):
        self.profile.points = 0
        self.assertEqual(self.profile.get_points_str(), '0')

        self.profile.points = 1000
        self.assertEqual(self.profile.get_points_str(), '1,000')

        self.profile.points = 1000000
        self.assertEqual(self.profile.get_points_str(), '1,000,000')

class GoalModelTests(TestCase):
    """Tests for Goal model class"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')
        cls.profile = Profile.objects.create(user=cls.user)
        
        cls.goal = Goal.objects.create(title='test goal', 
                                        description='test description', 
                                        deadline=get_week_from_today(), 
                                        priority=2, 
                                        progress=50.0,
                                        profile=cls.profile)
        
    def test_get_progress_str(self):
        self.goal.progress = 50.0
        self.assertEqual(self.goal.get_progress_str(), '50%')

        self.goal.progress = 75.2495
        self.assertEqual(self.goal.get_progress_str(), '75.25%')

    def test_get_deadline_str(self):
        self.goal.deadline = date(2023, 11, 5)
        self.assertEqual(self.goal.get_deadline_str(), 'November 05, 2023')

    def test_get_completed_str(self):
        self.goal.completed = date(2023, 11, 5)
        self.assertEqual(self.goal.get_completed_str(), 'November 05, 2023')

    def test_get_title_str(self):
        self.assertEqual(self.goal.get_title_str(), 'test goal')
       
        str_len = 30
        self.goal.title = 'this is a veeeeeeeeeeeeeeeeeeeeeeeeery long title'
        self.assertEqual(len(self.goal.get_title_str()), str_len + 3)

    def test_calculate_points(self):
        self.goal.completed = date.today()
        points_target = 34000
        self.assertEqual(points_target, self.goal.calculate_points())

        # min possible
        self.goal.priority = 1
        self.goal.completed = date.today() + timedelta(days=100)
        points_target = 10000
        self.assertEqual(points_target, self.goal.calculate_points())

        # max possible
        self.goal.priority = 3
        self.goal.completed = date.today() - timedelta(days=100)
        points_target = 60000
        self.assertEqual(points_target, self.goal.calculate_points())

    def test_add_and_undo_points(self):
        self.goal.completed = date.today()
        points_target = 34000

        self.goal.add_points()
        self.assertEqual(points_target, self.profile.points)

        self.goal.undo_points()
        self.assertEqual(0, self.profile.points)

    def test_complete_goal(self):
        self.goal.complete_goal()
        
        self.assertEqual(self.goal.completed, date.today())
        self.assertEqual(self.goal.progress, 100.0)
        self.assertEqual(self.profile.points, self.goal.calculate_points())

    def test_undo_complete(self):
        self.goal.complete_goal()
        self.goal.undo_complete()

        self.assertEqual(self.goal.completed, None)
        self.assertEqual(self.profile.points, 0)