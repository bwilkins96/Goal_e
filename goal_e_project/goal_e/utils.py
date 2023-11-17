# Utility functions

from datetime import date, timedelta

def prepare_goal_params(request):
    return [
        request.POST['title'],
        request.POST['description'],
        request.POST['deadline'],
        request.POST['priority'],
        request.POST['progress'],
    ]

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