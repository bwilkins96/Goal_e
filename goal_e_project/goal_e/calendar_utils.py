import calendar

def get_prev_month_year(month: int, year: int):
    if month == 1:
        return (12, year-1)
    
    return (month-1, year)

def get_next_month_year(month: int, year: int):
    if month == 12:
        return (1, year+1)

    return (month+1, year)

class MonthCalendar:
    def __init__(self, month: int, year: int):
        self.data = self._get_calendar_data(month, year)

    def _pad_calendar_data(self, data: list, rows: int):
        while len(data) < rows:
            data.append([0] * 7)
    
    def _convert_data(self, data: list):
        for week in data:
            for i, day in enumerate(week):
                week[i] = [day, True if day else False]
        
    def _get_calendar_data(self, month: int, year: int) -> list:
        data = calendar.monthcalendar(year, month)
        
        self._pad_calendar_data(data, 6)
        self._convert_data(data)

        # Add days from previous month
        if 0 == data[0][0][0]:
            prev_month, prev_year = get_prev_month_year(month, year)
            day_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
            
            for i in range(len(data[0])-1, -1, -1):            
                if data[0][i][0]: continue

                data[0][i][0] = day_in_prev_month
                day_in_prev_month -= 1

        # Add days from next month
        if 0 == data[-1][-1][0]:
            day_in_next_month = 1

            for data_idx in range(-2, 0):

                for i in range(len(data[data_idx])):
                    if data[data_idx][i][0]: continue

                    data[data_idx][i][0] = day_in_next_month
                    day_in_next_month += 1

        return data