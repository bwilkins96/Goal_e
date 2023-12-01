from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..utils import *

class UtilityTests(TestCase):
    """Tests for utility functions in utils.py"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user')

    def test_user_already_exists(self):
        self.assertTrue(user_already_exists('test_user'))
        self.assertFalse(user_already_exists('this_user_does_not_exist'))

    def test_valid_username(self):
        self.assertTrue(valid_username('test_user@-.+'))
        self.assertTrue(valid_username('@_username_with_30_characters_'))

        self.assertFalse(valid_username('username with spaces'))
        self.assertFalse(valid_username('username_with_more_than_30_characters'))

    def test_get_user_errors(self):
        errors = get_user_errors('test_user2', 'password', 'password')
        self.assertFalse(errors)

        errors = get_user_errors('test_user', 'password', 'different_password')
        self.assertTrue(errors)
        self.assertIn('user', errors)
        self.assertIn('password', errors)

        errors = get_user_errors('invalid//  username', 'password', 'password')
        self.assertTrue(errors)
        self.assertIn('user', errors)
        self.assertNotIn('password', errors)

        errors = get_user_errors('test_user', '', '', self.user)
        self.assertFalse(errors)

    def test_url_equals_reversed(self):
        test_url = 'http://goal-e.com' + reverse('goal_e:past_goals')
       
        self.assertTrue(url_equals_reversed(test_url, 'goal_e:past_goals'))
        self.assertFalse(url_equals_reversed(test_url, 'goal_e:index'))

    def test_num_str_with_commas(self):
        self.assertEqual(num_str_with_commas(0), '0')
        self.assertEqual(num_str_with_commas(1000), '1,000')
        self.assertEqual(num_str_with_commas(1000000.56), '1,000,000.56')

    def test_get_yyyy_mm_dd(self):
        nov51996 = date(1996, 11, 5)
        self.assertEqual(get_yyyy_mm_dd(nov51996), '1996-11-05')

    def test_get_full_date(self):
        nov51996 = date(1996, 11, 5)
        self.assertEqual(get_full_date(nov51996), 'November 05, 1996')

    def test_get_week_from_today(self):
        week_from_today = date.today() + timedelta(days=7)
        self.assertEqual(week_from_today, get_week_from_today())

    def test_add_years(self):
        leap_year_date = date(2024, 2, 29)
        
        expected = date(2025, 3, 1)
        self.assertEqual(add_years(leap_year_date, 1), expected)

        expected = date(2028, 2, 29)
        self.assertEqual(add_years(leap_year_date, 4), expected)

    def test_days_before(self):
        nov1 = date(2023, 11, 1)
        nov8 = date(2023, 11, 8)
        oct25 = date(2023, 10, 25)

        self.assertEqual(days_before(nov1, nov8), 7)
        self.assertEqual(days_before(oct25, nov8), 14)

    def test_get_prev_month_year(self):
        self.assertEqual(get_prev_month_year(5, 2023), (4, 2023))
        self.assertEqual(get_prev_month_year(1, 2023), (12, 2022))

    def get_next_month_year(self):
        self.assertEqual(get_next_month_year(5, 2023), (6, 2023))
        self.assertEqual(get_next_month_year(12, 2023), (1, 2024))

    def test_get_month_input_val(self):
        self.assertEqual(get_month_input_val(11, 2023), '2023-11')
        self.assertEqual(get_month_input_val(5, 2023), '2023-05')

    def test_last_of_month(self):
        self.assertEqual(last_of_month(12, 2023), 31)
        self.assertEqual(last_of_month(2, 2023), 28)
        self.assertEqual(last_of_month(2, 2024), 29)