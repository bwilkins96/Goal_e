from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import Profile, Goal
from ..utils import get_week_from_today

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

        self.client.post(self.urls_logged_in['new_goal'], self.valid_goal_req)
        new_goal = Goal.objects.filter(id=3).first()   

        self.assertTrue(new_goal)

        with self.assertRaises(ValidationError):
            self.client.post(self.urls_logged_in['new_goal'], self.invalid_goal_req)

    def test_edit_goal(self):
        self.client.login(username='test_user', password='password')
        
        self.client.post(reverse('goal_e:edit_goal', args=[1]), self.valid_goal_req)
        edited_goal = Goal.objects.get(id=1)
        
        self.assertEqual(edited_goal.title, 'valid goal')

        with self.assertRaises(ValidationError):
            self.client.post(reverse('goal_e:edit_goal', args=[1]), self.invalid_goal_req)

    def test_delete_goal(self):
        self.client.login(username='test_user', password='password')        
        self.client.post(reverse('goal_e:delete_goal'), {'id': 1})

        deleted = Goal.objects.filter(id=1).first()
        self.assertFalse(deleted)

    def test_complete_goal(self):
        self.client.login(username='test_user', password='password')        
        self.client.post(reverse('goal_e:complete_goal', args=[1]), {'id': 1})
        
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