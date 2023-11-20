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
    path('signup', views.signup, name='signup')
]