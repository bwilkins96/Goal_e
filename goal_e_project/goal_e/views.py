from django.shortcuts import render, get_object_or_404
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

        goal = Goal.objects.create(title=title, 
                                   description=description, 
                                   deadline=deadline, 
                                   priority=priority, 
                                   progress=progress)
        
        if float(goal.progress) == 100.0:
            goal.complete_goal()
            goal.save()
        
        return HttpResponseRedirect(reverse('goal_e:index'))

    return render(request, 'goal_e/new_goal.html')

def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)

    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)

        goal.title = title
        goal.description = description
        goal.deadline = deadline
        goal.priority = priority
        goal.progress = progress

        if float(goal.progress) == 100.0:
            goal.complete_goal()
        
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
        
        goal = get_object_or_404(Goal, id=goal_id)
        goal.delete()

    return HttpResponseRedirect(reverse('goal_e:index'))

def complete_goal(request, goal_id):
    response = {'error': 'operation unsuccessful'}

    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id)

        goal.complete_goal()
        goal.save()

        response = {
            'pointsAdded': 15000,
            'newPointsTotal': 30000,
            'dateStr': goal.get_completed_str(),
            'title': goal.title
        }

    return JsonResponse(response)

def resource_not_found(request, exception=None):
    if 'goals' in request.path:
        title = 'Goal Not Found'
    else:
        title = '404: Page Not Found'

    response = render(request, 'goal_e/not_found.html', { 'title': title })
    response.status_code = 404

    print(request.path)

    return response 