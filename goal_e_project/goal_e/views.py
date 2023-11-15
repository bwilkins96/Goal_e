from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Goal

def index(request):
    goal_list = Goal.objects.filter(completed=None).order_by('deadline', '-priority')

    context = {
        'title': 'Current Goals',
        'goal_list': goal_list
    }

    return render(request, 'goal_e/index.html', context)

def past_goals(request):
    goal_list = Goal.objects.exclude(completed=None).order_by('deadline', '-priority')

    context = {
        'title': 'Past Goals',
        'goal_list': goal_list
    }

    return render(request, 'goal_e/index.html', context)

def prepare_goal_params(request):
    title = request.POST['title']
    description = request.POST['description']
    deadline = request.POST['deadline']
    priority = request.POST['priority']
    progress = request.POST['progress']

    params = [title, description, deadline, priority, progress]
    return params

def new_goal(request):
    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)

        new_goal = Goal(title=title, 
                        description=description, 
                        deadline=deadline, 
                        priority=priority, 
                        progress=progress)
        
        new_goal.save()
        return HttpResponseRedirect(reverse('goal_e:index'))

    return render(request, 'goal_e/new_goal.html')