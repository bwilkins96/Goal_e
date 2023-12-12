from datetime import date
from json import loads

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Goal, Profile
from .goal_calendar import GoalCalendar, GoalCalendarNode

from .utils import (
    prepare_goal_params, 
    get_yyyy_mm_dd, 
    get_week_from_today_str, 
    add_years, 
    num_str_with_commas,
    get_prev_action,
    redirect_when_logged_in,
    get_user_errors,
    get_full_date,
    previous_url,
    get_prev_url,
    url_equals_reversed,
    get_next_month_year,
    get_prev_month_year,
    get_month_input_val,
    user_already_exists,
    valid_username
)

@login_required
def index(request: HttpRequest):
    profile = request.user.profile
    goal_list = Goal.objects.filter(profile=profile, completed=None).order_by('deadline', '-priority')

    context = {
        'title': 'Current Goals',
        'goal_list': goal_list,
        'prev_action': get_prev_action(request)
    }

    return render(request, 'goal_e/index.html', context)

@login_required
def past_goals(request: HttpRequest):
    profile = request.user.profile
    goal_list = Goal.objects.filter(profile=profile).exclude(completed=None).order_by('-completed', '-priority')

    context = {
        'title': 'Past Goals',
        'goal_list': goal_list,
        'prev_action': get_prev_action(request)
    }

    return render(request, 'goal_e/index.html', context)

@login_required
def new_goal(request: HttpRequest):
    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)
        profile = request.user.profile

        goal = Goal(title=title, 
                    description=description, 
                    deadline=deadline, 
                    priority=priority, 
                    progress=progress,
                    profile=profile)
        
        goal.full_clean()
        if goal.progress == 100.0:
            goal.complete_goal()
            
        goal.save()
        request.session['prev_action'] = ('Goal Set!', 'blue')
        return HttpResponseRedirect(reverse('goal_e:index'))

    context = { 
        'default_date': get_week_from_today_str(),
        'min_date': get_yyyy_mm_dd(date.today()),
        'max_date': get_yyyy_mm_dd(add_years(date.today(), 100)),
        'prev_url': get_prev_url(request, False)
        }
   
    return render(request, 'goal_e/new_goal.html', context)

@login_required
def edit_goal(request: HttpRequest, goal_id: int):
    profile = request.user.profile
    goal = get_object_or_404(Goal, id=goal_id, profile=profile)

    if request.method == 'POST':
        [title, description, deadline, priority, progress] = prepare_goal_params(request)

        goal.title = title
        goal.description = description
        goal.deadline = deadline
        goal.priority = priority
        goal.progress = progress

        goal.full_clean()

        completion_undone = False
        if (goal.progress == 100.0) and (not goal.completed):
            goal.complete_goal()
        elif goal.completed and (goal.progress < 100.0):
            goal.undo_complete()
            completion_undone = True
        
        goal.save()
        
        prev_url = get_prev_url(request)
        if goal.completed and url_equals_reversed(prev_url, 'goal_e:index'):
            response = HttpResponseRedirect(reverse('goal_e:past_goals') + f'#{goal.id}')
        elif completion_undone and url_equals_reversed(prev_url, 'goal_e:past_goals'):
            response = HttpResponseRedirect(reverse('goal_e:index') + f'#{goal.id}')
        else:
            response = HttpResponseRedirect(prev_url + f'#{goal.id}')

        return response

    today = date.today()
    min_date = min(goal.deadline, today)
    
    context = {
        'goal': goal,
        'date_val': get_yyyy_mm_dd(goal.deadline),
        'min_date': get_yyyy_mm_dd(min_date),
        'max_date': get_yyyy_mm_dd(add_years(today, 100))
    }

    request.session['prev_url'] = previous_url(request)
    return render(request, 'goal_e/edit_goal.html', context)

@login_required
def delete_goal(request: HttpRequest):
    if request.method == 'POST':
        goal_id = request.POST['id']
        profile = request.user.profile
        
        goal = get_object_or_404(Goal, id=goal_id, profile=profile)
        goal.delete()

        request.session['prev_action'] = ('Goal Deleted', 'red')

    return HttpResponseRedirect(get_prev_url(request))

@login_required
def complete_goal(request: HttpRequest, goal_id: int):
    response = {'error': 'operation unsuccessful'}

    if request.method == 'POST':
        profile = request.user.profile
        goal = get_object_or_404(Goal, id=goal_id, profile=profile)

        points = goal.complete_goal()
        goal.save()

        response = {
            'pointsAdded': num_str_with_commas(points),
            'newPointsTotal': goal.profile.get_points_str(),
            'dateStr': goal.get_completed_str(),
            'title': goal.get_title_str()
        }

    return JsonResponse(response)

@login_required
def resource_not_found(request: HttpRequest, exception=None):
    if 'goals' in request.path:
        title = 'Goal Not Found'
    else:
        title = '404: Page Not Found'

    response = render(request, 'goal_e/not_found.html', { 'title': title })
    response.status_code = 404

    return response 

@redirect_when_logged_in
def signup_view(request: HttpRequest):
    context = {}
    status_code = 200

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_conf = request.POST['confirmPassword']

        errors = get_user_errors(username, password, password_conf)

        if not errors:
            user = User.objects.create_user(username, password=password)
            profile = Profile.objects.create(user=user)

            login(request, user)
            return HttpResponseRedirect(reverse('goal_e:index'))
        else:
            context = {
                'username': username,
                'errors': errors
            }

            status_code = 400

    response = render(request, 'auth/signup.html', context)
    response.status_code = status_code

    return response

@redirect_when_logged_in
def login_view(request: HttpRequest):
    context = {}
    status_code = 200

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('goal_e:index'))
        else:
            context = {
                'username': username,
                'message': 'Invalid username and/or password'
            }

            status_code = 401 
    
    response = render(request, 'auth/login.html', context)
    response.status_code = status_code
    
    return response

@login_required
def sign_out_view(request: HttpRequest):
    logout(request)

    return HttpResponseRedirect(reverse('goal_e:login'))

@login_required
def calendar_view(request: HttpRequest, month: int = None, year: int = None):
    profile = request.user.profile
    today = date.today()

    if not (month or year):
        month = today.month
        year = today.year

    date_plus_100 = add_years(today, 100)
    max_date = get_month_input_val(date_plus_100.month, date_plus_100.year)

    today_id = None
    if month == today.month and year == today.year:
        today_id = f'True{today.day}'

    context = {
        'month_input_val': get_month_input_val(month, year),
        'calendar': GoalCalendar(month, year, profile, GoalCalendarNode).data,
        'next': get_next_month_year(month, year),
        'prev': get_prev_month_year(month, year),
        'month': month,
        'year': year,
        'max_date': max_date,
        'today_id': today_id
    }

    return render(request, 'goal_e/calendar.html', context)

@login_required
def daily_goals(request: HttpRequest, month: int, day: int, year: int):
    profile = request.user.profile
    day_date = date(year, month, day)
    goal_list = Goal.objects.filter(profile=profile, deadline=day_date).order_by('completed', '-priority')

    context = {
        'title': f'Goals for {get_full_date(day_date)}',
        'goal_list': goal_list,
        'prev_action': get_prev_action(request),
        'month': month,
        'year': year
    }

    return render(request, 'goal_e/index.html', context)

@login_required
def account_settings(request: HttpRequest):
    user = request.user
    profile = user.profile
    
    status_code = 200
    errors = None
    
    if request.method == 'POST':
        new_username = request.POST['username']
        new_pword = request.POST['password']
        new_pword_conf = request.POST['confirmPassword']
        new_theme = request.POST['theme']

        errors = get_user_errors(new_username, new_pword, new_pword_conf, user)

        if not errors:
            if user.username != new_username:
                user.username = new_username

            if new_pword:
                user.set_password(new_pword)

            if new_theme != profile.theme:
                profile.theme = new_theme

            profile.full_clean()
            user.save()
            profile.save()
            
            login(request, user)
            request.session['prev_action'] = ('Settings Saved', 'blue')
        else:
            request.session['prev_action'] = ('Error Saving Settings', 'red')
            status_code = 400

    context = { 
        'profile': profile,
        'prev_action': get_prev_action(request),
        'errors': errors
    }
    
    response = render(request, 'goal_e/acnt_settings.html', context)
    response.status_code = status_code

    return response

def username_available(request: HttpRequest):
    if request.method != 'POST':
        raise Http404

    available = True
    body = loads(request.body)
    username = body['username']

    if request.user.username == username:
        available = 'current username'
    elif user_already_exists(username):
        available = False
    elif not valid_username(username):
        available = 'invalid username'

    return JsonResponse({
        'username': username,
        'available': available
    })