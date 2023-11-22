from django.urls import path
from . import views

app_name = 'goal_e'
urlpatterns = [
    path('', views.index, name='index'),
    path('pastGoals', views.past_goals, name='past_goals'),
    path('newGoal', views.new_goal, name='new_goal'),
    path('goals/<int:goal_id>', views.edit_goal, name='edit_goal'),
    path('deleteGoal', views.delete_goal, name='delete_goal'),
    path('goals/<int:goal_id>/complete', views.complete_goal, name='complete_goal'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('signOut', views.sign_out_view, name='sign_out'),
    path('calendar/<int:month>/<int:year>', views.calendar_view, name='calendar'),
    path('calendar', views.calendar_view, name='calendar_default')
]