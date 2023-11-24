# Goal calendar class for monthly calendar data

from calendar import monthcalendar
from datetime import date

from .models import Goal, Profile
from .utils import last_of_month, get_prev_month_year

class GoalCalendarNode:
    def __init__(self, day: int, current_month: bool):
        self.day = day
        self.current_month = current_month
        self.goals = []

class GoalCalendar:
    def __init__(self, month: int, year: int, profile: Profile, node_class):
        self.node_class = node_class
        self._set_up_calendar_data(month, year, profile)

    def get_first_day_idx(self):
        for i, node in enumerate(self.data[0]):
            if node.day == 1:
                return i
            
    def get_week_day_idx(self, goal_day: int, first_day_idx: int):
        abs_idx = first_day_idx + goal_day - 1
        
        week_idx = abs_idx // 7
        day_idx = abs_idx % 7

        return (week_idx, day_idx)

    def _pad_calendar_data(self, rows: int):
        data = self.data

        while len(data) < rows:
            data.append([0] * 7)
    
    def _convert_data(self):
        for week in self.data:
            for i, day in enumerate(week):
                week[i] = self.node_class(day, True if day else False)
            
    def _add_goals_to_data(self, month: int, year: int, profile: Profile):
        data = self.data
        first = date(year, month, 1)
        last = date(year, month, last_of_month(month, year))

        goals = Goal.objects.filter(profile=profile, completed=None, deadline__gte=first, deadline__lte=last)

        first_day_idx = self.get_first_day_idx()
        for goal in goals:
            goal_day = goal.deadline.day
            
            week_idx, day_idx = self.get_week_day_idx(goal_day, first_day_idx) 
            data[week_idx][day_idx].goals.append(goal)
        
    def _set_up_calendar_data(self, month: int, year: int, profile: Profile) -> list:
        self.data = monthcalendar(year, month)
        data = self.data
        
        self._pad_calendar_data(6)
        self._convert_data()

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

        self._add_goals_to_data(month, year, profile)
        return data