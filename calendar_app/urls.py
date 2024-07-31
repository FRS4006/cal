from django.contrib import admin
from django.urls import path
from display import views as displayViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', displayViews.initial, name ="initial"),
    path('home/<int:input_selected_month>/<int:input_selected_year>/<int:input_selected_week>', displayViews.home, name ="home"),
    # This leads to the population of the selected month
    
    path('next_month/<int:next_month>/<int:selected_year>/<int:selected_week>', displayViews.next_month, name='next_month'),
    # This is to check that the next month is not in the next year, and then to display that next month
    path('previous_month/<int:previous_month>/<int:selected_year>/<int:selected_week>', displayViews.previous_month, name='previous_month'),
    # This is to check that the previous month is not in the previous year, and then to display that previous month

    path('next_week/<int:next_month>/<int:selected_month>/<int:selected_year>/<int:next_week>', displayViews.next_week, name='next_week'),
    # This is to check that the next week is not in the next month, and then to display that next week
    path('previous_week/<int:previous_month>/<int:selected_month>/<int:selected_year>/<int:previous_week>', displayViews.previous_week, name='previous_week'),
    # This is to check that the previous week is not in the previous month, and then to display that previous week

]
