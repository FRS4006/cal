from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CalendarEvent
from datetime import date
import calendar
import json


today = date.today()


def initial(request):
    # sets the initially displayed month to be the current month of the current year
    week = today.day//7
    return redirect('home', input_selected_month=today.month, input_selected_year=today.year, input_selected_week=week)



def month_logic(request, input_selected_month, input_selected_year, input_selected_week):
    selected_month = input_selected_month
    selected_year = input_selected_year
    selected_week = input_selected_week
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

        number_of_days_of_next_month = 42-date_info[1]
        display_first_day = previous_month_day_finder[1]
        # this removes the catch from the for loop that comes later

        # print(date_info[0], display_first_day)
        print(number_of_days_of_previous_month, previous_month_day_finder[1])

    else:
        number_of_days_of_next_month = 42 - number_of_days_of_previous_month - date_info[1]
        # the remainder of the number of days from the 35 grid minus the number of days from the previous month, minus the number of days of the current month
        display_first_day = previous_month_day_finder[1] - number_of_days_of_previous_month
        # set the first day in the display to be the total number of days in the month minus the number of days that will be displayed from the previous month

    previous_months_days = []
    current_months_days = []
    next_months_days = []
    all_days = []


    for day in range(display_first_day, previous_month_day_finder[1]):
        # this will be zero if there are 7 days in the previous week
        previous_months_days.append({'day': day+1, 'event': "", 'month':previous_month})
        all_days.append({'day': day+1, 'event': "", 'month':previous_month})
        # put the record of this number existing in the places it will be looked for
    for day in range(1, date_info[1]+1):
        # for the days in the month we are looking at add the days to the arrays
        current_months_days.append({'day': day, 'event': "", 'month':selected_month})
        all_days.append({'day': day, 'event': "", 'month':selected_month})

    for day in range(1, number_of_days_of_next_month+1):
        # for the number of days that will be displayed from the next month add the days to the arrays
        next_months_days.append({'day': day, 'event': "", 'month':next_month})
        all_days.append({'day': day, 'event': "", 'month':next_month})
    
    enumeration_test = list(enumerate(all_days, start=1))
    # for each of the days that are currently in order in the list of days to be displayed, make an array that contains all of their numbers's corresponding to index's in the list
    
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    fifth_week = []
    sixth_week = []
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
        elif(enumerator[0] < 36):
            fifth_week.append(enumerator[1])
        else:
            sixth_week.append(enumerator[1])
    return redirect()


def displayEventCreator(request, input_selected_month, input_selected_year, input_selected_week, next_month):
    calendarevent_all = CalendarEvent.objects.all()
    # find all of the events
    display_events = []
    # these will be the events that need to be displayed

    for event in calendarevent_all:
        if event.date_of_event.month == selected_month and event.date_of_event.year == selected_year:
            # if the month and year in the date are equal to the selected month and year add the event to the list of events to display
            string_date = event.date_of_event.strftime('%h/%d/%y')
            string_hour = event.date_of_event.strftime("%I:%M:%p")
            # date cannot be passed as json, so this turns it into a string

            display_events.append({'title': event.title, 'display_date': string_date, 'display_hour': string_hour, 'type': event.event_type, 'day': event.date_of_event.day, 'month': event.date_of_event.month, 'year': event.date_of_event.year, 'location': event.location, 'description': event.description, 'link': event.zoom_url})


        # elif event.date_of_event.month == previous_month and event.date_of_event.year == selected_year:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})


        # elif event.date_of_event.month == previous_month and event.date_of_event.year == selected_year-1:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})
    

        # elif event.date_of_event.month == next_month and event.date_of_event.year == selected_year:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})


        # elif event.date_of_event.month == next_month and event.date_of_event.year == selected_year+1:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})

        # these commented out pieces would be to add the logic for displaying from the past months and next months events as well
    json_display_events = json.dumps(display_events)

    return redirect()

def weekSelected():
    if(selected_week == 0):
        previous_week=5
        next_week=1
        # set the month to the previous month, then if the sixth week's first day is < 10 set the week to week 5 (selected_week =4) else selected week = 5
    elif(selected_week == 1):
        previous_week = 0
        next_week = 2
    elif(selected_week == 2):
        previous_week = 1
        next_week = 3
    elif(selected_week == 3):
        previous_week = 2
        next_week = 4
    elif(selected_week == 4):
        previous_week = 3
        next_week = 5
        if(sixth_week[0] and sixth_week[0]["day"] < 10):
            next_week = 0
            # and go to the next month
            selected_month+1
        else:
            next_week = 5

    elif(selected_week == 5):
        # check to see that the first day is not < 10 if it isnt, the next week is 0 and the previous one is 5, if it is, set the week to be the previous week
        if(sixth_week[0]["day"] > 10):
            previous_week = 4
            next_week = 0
        # the next week is the first week (selected_week=0) of the next month
        else:
            selected_week = 4
            previous_week = 3
            next_week = 0

        # when this logic is checked later, it should set the selected week to the previous week, so that a week from the current month is not populated again

        # can test in march / 2025



































def home(request, input_selected_month, input_selected_year, input_selected_week):
    selected_month = input_selected_month
    selected_year = input_selected_year
    selected_week = input_selected_week
    # will be subject to change based on selection



    # this can be a function


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



#  this can be a seperate funciton


    date_info = calendar.monthrange(selected_year, selected_month)
    # for selected month and year find the day of the week it starts on and the total number of days

    number_of_days_of_previous_month = date_info[0]+1
    # the number of days of the previous month is calculated by figuring out which day of the week the current week starts on (that day of the week is saved as a number)
    display_first_day = 0

    if(number_of_days_of_previous_month == 7):
        # if there are 7 days from the previous month in its last week, then the next month should be calculated simply using the number of days left over after subtracting the number of days in the month from 35

        number_of_days_of_next_month = 42-date_info[1]
        display_first_day = previous_month_day_finder[1]
        # this removes the catch from the for loop that comes later

        # print(date_info[0], display_first_day)
        print(number_of_days_of_previous_month, previous_month_day_finder[1])

    else:
        number_of_days_of_next_month = 42 - number_of_days_of_previous_month - date_info[1]
        # the remainder of the number of days from the 35 grid minus the number of days from the previous month, minus the number of days of the current month
        display_first_day = previous_month_day_finder[1] - number_of_days_of_previous_month
        # set the first day in the display to be the total number of days in the month minus the number of days that will be displayed from the previous month








    previous_months_days = []
    current_months_days = []
    next_months_days = []
    all_days = []


    for day in range(display_first_day, previous_month_day_finder[1]):
        # this will be zero if there are 7 days in the previous week
        previous_months_days.append({'day': day+1, 'event': "", 'month':previous_month})
        all_days.append({'day': day+1, 'event': "", 'month':previous_month})
        # put the record of this number existing in the places it will be looked for
    for day in range(1, date_info[1]+1):
        # for the days in the month we are looking at add the days to the arrays
        current_months_days.append({'day': day, 'event': "", 'month':selected_month})
        all_days.append({'day': day, 'event': "", 'month':selected_month})

    for day in range(1, number_of_days_of_next_month+1):
        # for the number of days that will be displayed from the next month add the days to the arrays
        next_months_days.append({'day': day, 'event': "", 'month':next_month})
        all_days.append({'day': day, 'event': "", 'month':next_month})

    









    calendarevent_all = CalendarEvent.objects.all()
    # find all of the events
    display_events = []
    # these will be the events that need to be displayed

    for event in calendarevent_all:
        if event.date_of_event.month == selected_month and event.date_of_event.year == selected_year:
            # if the month and year in the date are equal to the selected month and year add the event to the list of events to display
            string_date = event.date_of_event.strftime('%h/%d/%y')
            string_hour = event.date_of_event.strftime("%I:%M:%p")
            # date cannot be passed as json, so this turns it into a string

            display_events.append({'title': event.title, 'display_date': string_date, 'display_hour': string_hour, 'type': event.event_type, 'day': event.date_of_event.day, 'month': event.date_of_event.month, 'year': event.date_of_event.year, 'location': event.location, 'description': event.description, 'link': event.zoom_url})


        # elif event.date_of_event.month == previous_month and event.date_of_event.year == selected_year:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})


        # elif event.date_of_event.month == previous_month and event.date_of_event.year == selected_year-1:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})
    

        # elif event.date_of_event.month == next_month and event.date_of_event.year == selected_year:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})


        # elif event.date_of_event.month == next_month and event.date_of_event.year == selected_year+1:

        #     display_events.append({'type': event.event_type, 'day': event.date_of_event.day})

        # these commented out pieces would be to add the logic for displaying from the past months and next months events as well
    json_display_events = json.dumps(display_events)


#  can be a seperate function


   

    enumeration_test = list(enumerate(all_days, start=1))
    # for each of the days that are currently in order in the list of days to be displayed, make an array that contains all of their numbers's corresponding to index's in the list
    
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    fifth_week = []
    sixth_week = []
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
        elif(enumerator[0] < 36):
            fifth_week.append(enumerator[1])
        else:
            sixth_week.append(enumerator[1])




#  can be a seperate function



    if(selected_week == 0):
        previous_week=5
        next_week=1
        # set the month to the previous month, then if the sixth week's first day is < 10 set the week to week 5 (selected_week =4) else selected week = 5
    elif(selected_week == 1):
        previous_week = 0
        next_week = 2
    elif(selected_week == 2):
        previous_week = 1
        next_week = 3
    elif(selected_week == 3):
        previous_week = 2
        next_week = 4
    elif(selected_week == 4):
        previous_week = 3
        next_week = 5
        if(sixth_week[0] and sixth_week[0]["day"] < 10):
            next_week = 0
            # and go to the next month
            selected_month+1
        else:
            next_week = 5

    elif(selected_week == 5):
        # check to see that the first day is not < 10 if it isnt, the next week is 0 and the previous one is 5, if it is, set the week to be the previous week
        if(sixth_week[0]["day"] > 10):
            previous_week = 4
            next_week = 0
        # the next week is the first week (selected_week=0) of the next month
        else:
            selected_week = 4
            previous_week = 3
            next_week = 0

        # when this logic is checked later, it should set the selected week to the previous week, so that a week from the current month is not populated again

        # can test in march / 2025
            
    return render(request, 'hometwo.html', {'json_display_events': json_display_events, 'previous_week': previous_week, 'next_week': next_week,'selected_week': selected_week,'selected_year': selected_year,'selected_month': selected_month,'all_days': all_days, "first_week": first_week, 'second_week': second_week, 'third_week': third_week, 'fourth_week': fourth_week, 'fifth_week': fifth_week, 'sixth_week': sixth_week, 'display_events': display_events, 'next_month': next_month, 'previous_month': previous_month})


# to control the calendar buttons
def next_month(request, next_month, selected_year, selected_week):
    if(next_month == 1):
        selected_year = selected_year + 1
    #checking to see if the next year needs to be started


    return redirect('home', input_selected_month=next_month, input_selected_year=selected_year, input_selected_week = selected_week)


def previous_month(request, previous_month, selected_year, selected_week):
    if(previous_month == 12):
        selected_year = selected_year-1
        #checking to make sure that it does not have to go back to a previous year

    return redirect('home', input_selected_month=previous_month, input_selected_year=selected_year, input_selected_week = selected_week)

    

def next_week(request, next_month, selected_month, selected_year, next_week, selected_week):
    if request.method == 'POST':
        if(selected_week == 5):
            selected_month = next_month
            return redirect('next_month', next_month=next_month, selected_year=selected_year, selected_week=selected_week)
        print(next_month, selected_week+1)

    return redirect('home', input_selected_month=selected_month, input_selected_year=selected_year, input_selected_week = next_week)


def previous_week(request, previous_month, selected_month, selected_year, previous_week, selected_week):
    if request.method == 'POST':
        if (selected_week == 0):
            selected_month = previous_month
            print(previous_month)
            return redirect('previous_month', previous_month=previous_month, selected_year=selected_year, selected_week = previous_week)

    return redirect('home', input_selected_month=selected_month, input_selected_year=selected_year, input_selected_week = previous_week)
    