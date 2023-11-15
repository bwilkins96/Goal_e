from django.shortcuts import render

from .models import Goal

def index(request):
    goal_list = Goal.objects.filter(completed=None).order_by('deadline', '-priority')

    context = {
        'title': 'Current Goals',
        'goal_list': goal_list
    }

    return render(request, 'goal_e/index.html', context)

def pastGoals(request):
    goal_list = Goal.objects.exclude(completed=None).order_by('deadline', '-priority')

    context = {
        'title': 'Past Goals',
        'goal_list': goal_list
    }

    return render(request, 'goal_e/index.html', context)