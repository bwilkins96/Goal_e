# Utility functions

from calendar import monthrange
from collections import defaultdict
from datetime import date, timedelta

from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User

def prepare_goal_params(request: HttpRequest) -> list:
    return [
        request.POST['title'],
        request.POST['description'],
        request.POST['deadline'],
        request.POST['priority'],
        request.POST['progress'],
    ]

def user_already_exists(username: str) -> bool:
    prev_user = User.objects.filter(username=username)
    return bool(prev_user)

def valid_username(username: str) -> bool:
    if len(username) > 30: return False
    allowed = set(['_', '@', '+', '.', '-'])

    for char in username:
        if not (char.isalnum() or char in allowed):
            return False
        
    return True

def get_user_errors(username: str, password: str, password_conf: str, user: User = None):
    errors = defaultdict(list)
    check_username_available = (user is None) or (user.username != username)

    if check_username_available and user_already_exists(username):
        errors['user'].append('Username already exists')
    elif not valid_username(username):
        errors['user'].append('Username may have letters / numbers / _ - @ + .')

    if password != password_conf:
        errors['password'].append('Passwords do not match')

    return errors

def redirect_when_logged_in(func):
    def inner(request: HttpRequest):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('goal_e:index'))

        return func(request)
    
    return inner

def get_prev_action(request: HttpRequest):
    prev_action = request.session.get('prev_action')
    request.session['prev_action'] = None

    return prev_action

def previous_url(request: HttpRequest):
    return request.META.get('HTTP_REFERER')

def get_prev_url(request: HttpRequest, session=True):
    if session:
        url = request.session.get('prev_url')
    else:
        url = previous_url(request)

    if url:
        return url
    
    return reverse('goal_e:index')

def url_equals_reversed(url: str, reverse_str: str):
    return url.endswith(reverse(reverse_str))

def num_str_with_commas(num: int | float) -> str:
    return f'{num:,}'

# Date / calendar related functions 
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
    if (date_inst.month == 2) and (date_inst.day == 29) and (years % 4 != 0):
        date_inst = date_inst.replace(month = 3, day = 1) 

    date_inst = date_inst.replace(year = date_inst.year + years)

    return date_inst

def days_before(start: date, end: date) -> int:
    diff = end - start 
    return diff.days

def get_prev_month_year(month: int, year: int):
    if month == 1:
        return (12, year-1)
    
    return (month-1, year)

def get_next_month_year(month: int, year: int):
    if month == 12:
        return (1, year+1)

    return (month+1, year)

def get_month_input_val(month: int, year: int):
    if month < 10:
        month = f'0{month}'

    return f'{year}-{month}'

def last_of_month(month: int, year: int):
    return monthrange(year, month)[1]