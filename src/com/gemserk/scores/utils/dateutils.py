'''
Created on 12/08/2010

@author: gemserk
'''

import datetime
import calendar

# type could be day/week/month

def get_datetime_range(type):
    
    today = datetime.datetime.today()
    
    # I dont want other information like minutes/hour/etc
    today = datetime.datetime(today.year,today.month,today.day)
    
    if (type == "day"):
        begin = today
        end = begin + datetime.timedelta(days=1)
        return begin, end

    if (type == "week"):
        weekday = today.weekday()
        begin = today - datetime.timedelta(days=weekday)
        end = begin + datetime.timedelta(weeks=1)
        return begin, end
    
    if (type == "month"):
        month_days = calendar.monthrange(today.year, today.month)[1]
        begin = datetime.datetime(today.year,today.month,1)
        end = begin + datetime.timedelta(days=month_days)
        return begin, end

    return today, today

