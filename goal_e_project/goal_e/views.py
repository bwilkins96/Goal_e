from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import Goal
from .utils import prepare_goal_params, get_yyyy_mm_dd

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

def new_goal(request):
    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)

        Goal.objects.create(title=title, 
                            description=description, 
                            deadline=deadline, 
                            priority=priority, 
                            progress=progress)
        
        return HttpResponseRedirect(reverse('goal_e:index'))

    return render(request, 'goal_e/new_goal.html')

def edit_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)

    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)

        goal.title = title
        goal.description = description
        goal.deadline = deadline
        goal.priority = priority
        goal.progress = progress
        
        goal.save()
    
    goal = Goal.objects.get(id=goal_id)

    context = {
        'goal': goal,
        'date_val': get_yyyy_mm_dd(goal.deadline)
    }

    return render(request, 'goal_e/edit_goal.html', context)

def delete_goal(request):
    if request.method == 'POST':
        goal_id = request.POST['id']
        
        goal = Goal.objects.get(id=goal_id)
        if goal: goal.delete()

    return HttpResponseRedirect(reverse('goal_e:index'))

def complete_goal(request, goal_id):
    response = {'error': 'operation unsuccessful'}

    if request.method == 'POST':
        goal = Goal.objects.get(id=goal_id)

        goal.complete_goal()
        goal.save()

        response = {
            'pointsAdded': 15000,
            'newPointsTotal': 30000,
            'dateStr': goal.get_completed_str()
        }

    return JsonResponse(response)

