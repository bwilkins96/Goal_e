from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile, Goal
from ..goal_calendar import GoalCalendar, GoalCalendarNode

class GoalCalendarTests(TestCase):
    """Tests for GoalCalendar class"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')
        cls.profile = Profile.objects.create(user=cls.user)
        
        cls.goal = Goal.objects.create(title='test goal', 
                                       description='test description', 
                                       deadline=date(2023, 11, 1), 
                                       priority=2, 
                                       progress=50.0,
                                       profile=cls.profile)
        
        cls.calendar = GoalCalendar(11, 2023, cls.profile, GoalCalendarNode)

    def test_data(self):
        first = self.calendar.data[0][0]
        self.assertEqual(first.day, 30)
        self.assertFalse(first.current_month)
        self.assertEqual(len(first.goals), 0)

        last = self.calendar.data[-1][-1]
        self.assertEqual(last.day, 10)
        self.assertFalse(last.current_month)
        self.assertEqual(len(last.goals), 0)

        nov1_idx = self.calendar.get_first_day_idx()
        nov1 = self.calendar.data[0][nov1_idx]
        self.assertEqual(nov1.day, 1)
        self.assertTrue(nov1.current_month)
        self.assertEqual(len(nov1.goals), 1)

    def test_get_first_day_idx(self):
        expected = 2
        actual = self.calendar.get_first_day_idx()

        self.assertEqual(expected, actual)

    def test_get_week_day_idx(self):
        first_day_idx = self.calendar.get_first_day_idx()
        week_idx, day_idx = self.calendar.get_week_day_idx(15, first_day_idx)

        self.assertEqual(week_idx, 2)
        self.assertEqual(day_idx, 2)
