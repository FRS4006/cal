from django.contrib import admin
from django.urls import path
from display import views as displayViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', displayViews.initial, name ="initial"),
    path('home/<int:input_selected_month>/<int:input_selected_year>', displayViews.home, name ="home"),
    # This leads to the population of the selected month
    
    path('next/<int:next_month>/<int:selected_year>', displayViews.next, name='next'),
    # This is to check that the next month is not in the next year, and then to display that next month
    path('previous/<int:previous_month>/<int:selected_year>', displayViews.previous, name='previous')
    # This is to check that the previous month is not in the previous year, and then to display that previous month

]
