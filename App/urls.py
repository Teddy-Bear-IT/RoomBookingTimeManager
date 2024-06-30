from django.urls import path

from .views import login,index, get_times_for_date , booking_time, logout

app_name='App'
urlpatterns = [
    path('',login,name='login'),
    path('work/',index,name='index'),
    path('get_times_for_room/<int:id_room>/<str:date_select>/',get_times_for_date,name='get_times_for_date'),
    path('booking_time/',booking_time,name='booking_time'),
    path('logout/',logout,name='logout'),

]