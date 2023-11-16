# Utility functions

from datetime import date

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