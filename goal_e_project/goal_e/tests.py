from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile, Goal
from .goal_calendar import GoalCalendar, GoalCalendarNode

from .utils import get_week_from_today

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
       
        str_len = 20
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

class ViewTests(TestCase):
    """Tests for behavior of views"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='password')
        cls.profile = Profile.objects.create(user=cls.user)

        cls.user2 = User.objects.create_user(username='test_user2', password='password2')
        cls.profile2 = Profile.objects.create(user=cls.user2)
        
        cls.goal = Goal.objects.create(title='test goal', 
                                        description='test description', 
                                        deadline=get_week_from_today(), 
                                        priority=2, 
                                        progress=50.0,
                                        profile=cls.profile)
        
        cls.goal2 = Goal.objects.create(title='test goal 2', 
                                        description='test description 2', 
                                        deadline=get_week_from_today(), 
                                        priority=2, 
                                        progress=50.0,
                                        profile=cls.profile2)
        
        cls.urls_logged_in = {
            'index': reverse('goal_e:index'),
            'past_goals': reverse('goal_e:past_goals'),
            'new_goal': reverse('goal_e:new_goal'),
            'calendar_default': reverse('goal_e:calendar_default'),
            'calendar_daily_goals': reverse('goal_e:daily_goals', args=[11, 5, 2023]),
            'account_settings': reverse('goal_e:account_settings'),
        }

        cls.urls_logged_out = {
            'signup': reverse('goal_e:signup'),
            'login': reverse('goal_e:login'),
        }

        cls.valid_goal_req = {
            'title': 'valid goal', 
            'description': '', 
            'deadline': date.today(), 
            'priority': 2, 
            'progress': 50.0,
        }

        cls.invalid_goal_req = {
            'title': 'invalid goal', 
            'description': '', 
            'deadline': 'this is a string!', 
            'priority': -50, 
            'progress': 5000000.0,
        }
        
    def test_login_required(self):
        urls =  self.urls_logged_in.values()
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user', password='password')

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_redirect_when_logged_in(self):
        urls = self.urls_logged_out.values()
        self.client.login(username='test_user', password='password')

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        self.client.logout()
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_user_can_only_access_own_goals(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get(self.urls_logged_in['index'])

        goal_list = response.context['goal_list']
        self.assertTrue(self.goal in goal_list)
        self.assertFalse(self.goal2 in goal_list)

        response = self.client.get(reverse('goal_e:edit_goal', args=[1]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('goal_e:edit_goal', args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_index(self):
        self.client.login(username='test_user', password='password')

        response = self.client.get(self.urls_logged_in['index'])
        goal_list = response.context['goal_list']
        self.assertEqual(len(goal_list), 1)

        self.goal.complete_goal()
        self.goal.save()

        response = self.client.get(self.urls_logged_in['index'])
        goal_list = response.context['goal_list']
        self.assertEqual(len(goal_list), 0)
        
    def test_past_goals(self):
        self.client.login(username='test_user', password='password')

        response = self.client.get(self.urls_logged_in['past_goals'])
        goal_list = response.context['goal_list']
        self.assertEqual(len(goal_list), 0)

        self.goal.complete_goal()
        self.goal.save()

        response = self.client.get(self.urls_logged_in['past_goals'])
        goal_list = response.context['goal_list']
        self.assertEqual(len(goal_list), 1)

    def test_new_goal(self):
        self.client.login(username='test_user', password='password')

        response = self.client.post(self.urls_logged_in['new_goal'], self.valid_goal_req)
        new_goal = Goal.objects.filter(id=3).first()   

        self.assertTrue(new_goal)

        with self.assertRaises(ValidationError):
            self.client.post(self.urls_logged_in['new_goal'], self.invalid_goal_req)

    def test_edit_goal(self):
        self.client.login(username='test_user', password='password')
        
        response = self.client.post(reverse('goal_e:edit_goal', args=[1]), self.valid_goal_req)
        edited_goal = Goal.objects.get(id=1)
        
        self.assertEqual(edited_goal.title, 'valid goal')

        with self.assertRaises(ValidationError):
            self.client.post(reverse('goal_e:edit_goal', args=[1]), self.invalid_goal_req)

    def test_delete_goal(self):
        self.client.login(username='test_user', password='password')        
        response = self.client.post(reverse('goal_e:delete_goal'), {'id': 1})

        deleted = Goal.objects.filter(id=1).first()
        self.assertFalse(deleted)

    def test_complete_goal(self):
        self.client.login(username='test_user', password='password')        
        response = self.client.post(reverse('goal_e:complete_goal', args=[1]), {'id': 1})
        
        completed = Goal.objects.filter(id=1).first()
        self.assertEqual(completed.completed, date.today())
        self.assertEqual(completed.progress, 100)

    def test_calendar_view(self):
        self.client.login(username='test_user', password='password')        
        response = self.client.get(self.urls_logged_in['calendar_default'])
        today = date.today()

        context = response.context
        self.assertEqual(context['year'], today.year)
        self.assertEqual(context['month'], today.month)

        response = self.client.get(reverse('goal_e:calendar', args=[1, 2024]))

        context = response.context
        self.assertEqual(context['year'], 2024)
        self.assertEqual(context['month'], 1)

    def test_daily_goals(self):
        self.client.login(username='test_user', password='password')

        today = date.today()
        response = self.client.get(reverse('goal_e:daily_goals', args=[today.month, today.day, today.year]))        
        
        goal_list = response.context['goal_list']
        self.assertEqual(len(goal_list), 0)

        deadline = get_week_from_today()
        response = self.client.get(reverse('goal_e:daily_goals', args=[deadline.month, deadline.day, deadline.year]))
        
        goal_list = response.context['goal_list']
        self.assertEqual(goal_list[0], self.goal)
        self.assertEqual(goal_list[0].deadline, deadline)

    def test_login_view(self):
        invalid_login = {'username': 'not_real_user', 'password': 'not_real_password'}
        response = self.client.post(self.urls_logged_out['login'], invalid_login)

        self.assertEqual(response.status_code, 401)

        valid_login = {'username': 'test_user', 'password': 'password'}
        response = self.client.post(self.urls_logged_out['login'], valid_login)
        
        self.assertEqual(response.wsgi_request.user, self.user)
        self.assertRedirects(response, self.urls_logged_in['index'], 302)

    def test_signup_view(self):
        non_matching_passwords = {
            'username': 'test_user3',
            'password': 'password',
            'confirmPassword': 'non_matching_password'
        }

        response = self.client.post(self.urls_logged_out['signup'], non_matching_passwords)
        self.assertEqual(response.status_code, 400)

        username_exists = {
            'username': 'test_user',
            'password': 'password',
            'confirmPassword': 'password'
        }

        response = self.client.post(self.urls_logged_out['signup'], username_exists)
        self.assertEqual(response.status_code, 400)

        valid_sign_up = {
            'username': 'test_user3',
            'password': 'password',
            'confirmPassword': 'password'
        }

        response = self.client.post(self.urls_logged_out['signup'], valid_sign_up)
        self.assertRedirects(response, self.urls_logged_in['index'], 302)

    def test_signout_view(self):
        self.client.login(username='test_user', password='password')
        
        response = self.client.get(self.urls_logged_in['index'])
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('goal_e:sign_out'))
        self.assertRedirects(response, self.urls_logged_out['login'], 302)

        response = self.client.get(self.urls_logged_in['index'])
        self.assertEqual(response.status_code, 302)

    def test_account_settings(self):
        self.client.login(username='test_user', password='password')

        valid_settings = {
            'username': 'test_user3',
            'password': 'new_password',
            'confirmPassword': 'new_password',
            'theme': 2
        }

        response = self.client.post(self.urls_logged_in['account_settings'], valid_settings)
        updated_user = User.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_user.username, 'test_user3')
        self.assertEqual(updated_user.profile.theme, 2)
        self.assertTrue(self.client.login(username='test_user3', password='new_password')) 


        invalid_settings = {
            'username': 'test_user2',
            'password': 'new_password_2',
            'confirmPassword': 'non_matching_new_password',
            'theme': 1
        }

        response = self.client.post(self.urls_logged_in['account_settings'], invalid_settings)
        updated_user = User.objects.get(id=1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(updated_user.username, 'test_user3')
        self.assertEqual(updated_user.profile.theme, 2) 
        self.assertFalse(self.client.login(username='test_user3', password='new_password_2')) 

    def test_username_available(self):
        response = self.client.get(reverse('goal_e:username_available', args=['test_user3'])).json()
        self.assertTrue(response['available'])

        response = self.client.get(reverse('goal_e:username_available', args=['test_user'])).json()
        self.assertFalse(response['available'])

        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('goal_e:username_available', args=['test_user'])).json()
        self.assertEqual(response['available'], 'current username')




        
        


        
