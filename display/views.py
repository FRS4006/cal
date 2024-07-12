from django.shortcuts import render
from django.http import HttpResponse
import calendar 

def home(request):
    selected_month = 7
    selected_year = 2024

    first_day_finder = calendar.monthrange(selected_year, selected_month)
    number_of_days_of_previous_month = first_day_finder[0]+1

    if(number_of_days_of_previous_month == 7):
        number_of_days_of_next_month = 35-first_day_finder[1]
    else:
        number_of_days_of_next_month = 35-number_of_days_of_previous_month-first_day_finder[1]


    if(selected_month==1):
        previous_month=12
    else:
        previous_month = selected_month - 1
    
    if(selected_month==12):
        next_month=1
    else:
        next_month = selected_month + 1

    if(selected_month == 1):
        previous_month_day_finder = calendar.monthrange(selected_year-1, previous_month)
    else:
        previous_month_day_finder = calendar.monthrange(selected_year, previous_month)

    previous_months_days = []
    current_month_days = []
    next_month_days = []
    display_first_day = previous_month_day_finder[1] - number_of_days_of_previous_month

    for day in range(display_first_day, previous_month_day_finder[1]):
        previous_months_days.append(day+1)

    for day in range(1, first_day_finder[1]+1):
        current_month_days.append(day)

    for day in range(1, number_of_days_of_next_month+1):
        next_month_days.append(day)

    print(number_of_days_of_previous_month, first_day_finder[1], number_of_days_of_next_month, display_first_day, "previous month:", previous_months_days, "current month:", current_month_days, "next month:", next_month_days)
    return render(request, 'hometwo.html')



# Create your views here.
