import calendar
from datetime import date

from .models import Goal, Profile

def get_prev_month_year(month: int, year: int):
    if month == 1:
        return (12, year-1)
    
    return (month-1, year)

def get_next_month_year(month: int, year: int):
    if month == 12:
        return (1, year+1)

    return (month+1, year)

def get_month_year_str(month: int, year: int):
    return f'{calendar.month_name[month]}, {year}'

def last_of_month(month: int, year: int):
    return calendar.monthrange(year, month)[1]

class GoalCalendarNode():
    def __init__(self, day: int, current_month: bool):
        self.day = day
        self.current_month = current_month
        self.goals = []

class GoalCalendar:
    def __init__(self, month: int, year: int, profile: Profile):
        self.data = self._get_calendar_data(month, year, profile)

    def _pad_calendar_data(self, data: list, rows: int):
        while len(data) < rows:
            data.append([0] * 7)
    
    def _convert_data(self, data: list):
        for week in data:
            for i, day in enumerate(week):
                week[i] = GoalCalendarNode(day, True if day else False)

    def _get_first_day_idx(self, data: list):
        for i, node in enumerate(data[0]):
            if node.day == 1:
                return i
            
    def _add_goals_to_data(self, data: list, month: int, year: int, profile: Profile):
        first = date(year, month, 1)
        last = date(year, month, last_of_month(month, year))

        goals = Goal.objects.filter(profile=profile, completed=None, deadline__gte=first, deadline__lte=last)

        first_day_idx = self._get_first_day_idx(data)
        for goal in goals:
            goal_day = goal.deadline.day
            
            abs_idx = first_day_idx + goal_day - 1
            week_idx = abs_idx // 7
            day_idx = abs_idx % 7

            data[week_idx][day_idx].goals.append(goal)
        
    def _get_calendar_data(self, month: int, year: int, profile: Profile) -> list:
        data = calendar.monthcalendar(year, month)
        
        self._pad_calendar_data(data, 6)
        self._convert_data(data)

        # Add days from previous month
        if 0 == data[0][0].day:
            prev_month, prev_year = get_prev_month_year(month, year)
            day_in_prev_month = last_of_month(prev_month, prev_year)
            
            for i in range(len(data[0])-1, -1, -1):            
                if data[0][i].day: continue

                data[0][i].day = day_in_prev_month
                day_in_prev_month -= 1

        # Add days from next month
        if 0 == data[-1][-1].day:
            day_in_next_month = 1

            for data_idx in range(-2, 0):

                for i in range(len(data[data_idx])):
                    if data[data_idx][i].day: continue

                    data[data_idx][i].day = day_in_next_month
                    day_in_next_month += 1

        self._add_goals_to_data(data, month, year, profile)
        return data