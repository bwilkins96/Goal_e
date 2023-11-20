# Utility functions

from datetime import date, timedelta

from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect

def prepare_goal_params(request: HttpRequest) -> list:
    return [
        request.POST['title'],
        request.POST['description'],
        request.POST['deadline'],
        request.POST['priority'],
        request.POST['progress'],
    ]

def get_prev_action(request: HttpRequest):
    prev_action = request.session.get('prev_action')
    request.session['prev_action'] = None

    return prev_action

def get_yyyy_mm_dd(date_inst: date) -> str:
    return date_inst.strftime('%Y-%m-%d')

def get_full_date(date_inst: date) -> str:
    return date_inst.strftime('%B %d, %Y')

def get_week_from_today() -> date:
    return date.today() + timedelta(days=7)

def get_week_from_today_str() -> str:
    next_week = get_week_from_today()
    return get_yyyy_mm_dd(next_week)

def add_years(date_inst: date, years: int) -> date:
    date_inst = date_inst.replace(year = date_inst.year + years)

    if (date_inst.month == 2) and (date_inst.day == 29):
        date_inst = date_inst.replace(month = 3, day = 1) 

    return date_inst

def days_before(start: date, end: date) -> int:
    diff = end - start 
    return diff.days

def num_str_with_commas(num: int | float) -> str:
    return f'{num:,}'

def redirect_when_logged_in(func):
    def inner(request: HttpRequest):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('goal_e:index'))

        return func(request)
    
    return inner