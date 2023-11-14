from django.shortcuts import render

from .models import Goal

def index(request):
    goal_list = Goal.objects.all()

    context = {
        'goal_list': goal_list
    }

    return render(request, 'goal_e/index.html', context)