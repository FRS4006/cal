from django.shortcuts import render
from django.http import HttpResponse
from .models import CalendarEvent
import calendar 

def home(request):
    selected_month = 7
    selected_year = 2024
    # will be subject to change based on selection

    if(selected_month==1):
        previous_month=12
        previous_month_day_finder = calendar.monthrange(selected_year-1, previous_month)

    else:
        previous_month = selected_month - 1
        previous_month_day_finder = calendar.monthrange(selected_year, previous_month)
    # make sure that previous month is changed correctly to match the year changing
    # make sure that previous year is changed correctly to match the month changing

    if(selected_month==12):
        next_month=1
    else:
        next_month = selected_month + 1
    # make sure that next month is changed correctly to match the year changing
    # the number of days in the next month does not have to be calculated, so the day finder is not needed


    date_info = calendar.monthrange(selected_year, selected_month)
    # for selected month and year find the day of the week it starts on and the total number of days

    number_of_days_of_previous_month = date_info[0]+1
    # the number of days of the previous month is calculated by figuring out which day of the week the current week starts on (that day of the week is saved as a number)
    display_first_day = 0

    if(number_of_days_of_previous_month == 7):
        # if there are 7 days from the previous month in its last week, then the next month should be calculated simply using the number of days left over after subtracting the number of days in the month from 35

        number_of_days_of_next_month = 35-date_info[1]
        display_first_day = previous_month_day_finder[1]
        # this removes the catch from the for loop that comes later

        # print(date_info[0], display_first_day)
        print(number_of_days_of_previous_month, previous_month_day_finder[1])

    else:
        number_of_days_of_next_month = 35 - number_of_days_of_previous_month - date_info[1]
        # the remainder of the number of days from the 35 grid minus the number of days from the previous month, minus the number of days of the current month
        display_first_day = previous_month_day_finder[1] - number_of_days_of_previous_month
        # set the first day in the display to be the total number of days in the month minus the number of days that will be displayed from the previous month

    previous_months_days = []
    current_months_days = []
    next_months_days = []
    all_days = []


    for day in range(display_first_day, previous_month_day_finder[1]):
        # this will be zero if there are 7 days in the previous week
        previous_months_days.append({'day': day+1, 'event': ""})
        all_days.append({'day': day+1, 'event': ""})
        # put the record of this number existing in the places it will be looked for
    for day in range(1, date_info[1]+1):
        # for the days in the month we are looking at add the days to the arrays
        current_months_days.append({'day': day, 'event': ""})
        all_days.append({'day': day, 'event': ""})

    for day in range(1, number_of_days_of_next_month+1):
        # for the number of days that will be displayed from the next month add the days to the arrays
        next_months_days.append({'day': day, 'event': ""})
        all_days.append({'day': day, 'event': ""})

    
    calendarevent_all = CalendarEvent.objects.all()
    # find all of the events
    display_events = []
    # these will be the events that need to be displayed

    for event in calendarevent_all:
        if event.date_of_event.month == selected_month and event.date_of_event.year == selected_year:
            # if the month and year in the date are equal to the selected month and year add the event to the list of events to display
            display_events.append({'type': event.event_type, 'day': event.date_of_event.day})
            for number in all_days:
                if event.date_of_event.day == number['day']:
                    number['event'] = event.event_type



    enumeration_test = list(enumerate(all_days, start=1))
    # for each of the days that are currently in order in the list of days to be displayed, make an array that contains all of their numbers's corresponding to index's in the list
    
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    fifth_week = []
    for enumerator in enumeration_test:
        # for each days position in the array it is checked for "week location" and then the date is added to that week
        if(enumerator[0] < 8):
            first_week.append(enumerator[1])
        elif(enumerator[0] < 15):
            second_week.append(enumerator[1])
        elif(enumerator[0] < 22):
            third_week.append(enumerator[1])
        elif(enumerator[0] < 29):
            fourth_week.append(enumerator[1])
        else:
            fifth_week.append(enumerator[1])

    print("events to display:", display_events, "total number of days populated for previous month:", number_of_days_of_previous_month,  "total number of days populated for next month:", number_of_days_of_next_month, "days from previous month:", previous_months_days, "days from current month:", current_months_days, "days from next month:", next_months_days)
    # print("First Week", first_week, "Second Week", second_week, "Third Week", third_week, "Fourth Week", fourth_week, "Fifth Week", fifth_week)
    return render(request, 'hometwo.html', {'all_days': all_days, "first_week": first_week, 'second_week': second_week, 'third_week': third_week, 'fourth_week': fourth_week, 'fifth_week': fifth_week, 'events_to_display': display_events})



# Create your views here.
