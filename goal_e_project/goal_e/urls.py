from django.urls import path
from . import views

app_name = 'goal_e'
urlpatterns = [
    path('', views.index, name='index'),
    path('pastGoals', views.pastGoals, name='past_goals')
]