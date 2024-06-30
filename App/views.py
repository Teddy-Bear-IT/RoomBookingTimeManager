import json
from datetime import datetime
from datetime import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

#import your forms here
from .forms import UserLoginForm


# import your model here.
from .models import Rooms, DateBookingRoom,TimesBooking
# Create your views here.

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('App:index'))

    else:
        form = UserLoginForm()
    context = {
        'form_authorization': form
    }
    return render(request,'App/login.html',context)

@login_required
def index(request):
    context = {
        'all_booking': list(Rooms.objects.all()),
    }
    return render(request,'App/index.html',context)

def get_times_for_date(request,id_room,date_select):
    """
        Общий вьюха для загрузки начальной страницы
        И выгрузки информации для выбранной даты

    """
    print("дата - ", date_select)
    if isinstance(date_select, str):
        date_select = datetime.strptime(date_select, '%Y-%m-%d').date()

    # получение объекта комнаты
    room_object = Rooms.objects.get(id=id_room)

    # проверяем, есть ли на этот день в этой комнате что-то(т.е. если ли в бд запись этой даты)
    room_date_exists = DateBookingRoom.objects.filter(room_fk=room_object, date=date_select).exists()
    if not room_date_exists:
        # если отсутствовала дата
        DateBookingRoom(room_fk=room_object, date=date_select).save()
        print("создал запись даты") # del later
    else:
        print("запись не нужна") # del later

    # получение объекта даты после проверок
    date_booking_object = DateBookingRoom.objects.get(room_fk=room_object, date=date_select)
    # получение времени по всем правилам
    times_rooming = TimesBooking.objects.filter(date_fk=date_booking_object).values('id',
                                                                                                          'time_start_booking',
                                                                                                          'time_finish_booking',
                                                                                                          'description_booking')
    print("Отдаю - ", list(times_rooming))
    return JsonResponse(list(times_rooming), safe=False)
def booking_time(request):
    def is_overlapping(interval1, interval2):
        start1, end1 = interval1.time_start_booking, interval1.time_finish_booking
        start2, end2 = interval2.time_start_booking, interval2.time_finish_booking

        return start1 < end2 and start2 < end1

    def is_time_available(start_time, end_time, intervals):
        new_interval = TimesBooking(time_start_booking=start_time, time_finish_booking=end_time, user_fk=None,date_fk=None)
        return not any(is_overlapping(new_interval, interval) for interval in intervals)


    if request.method=='POST':
        id_room = request.POST['id_room']
        date_book = datetime.strptime(request.POST['date_booking'], '%Y-%m-%d').date()
        time_start_book =  datetime.strptime(request.POST['time_start_booking'], '%H:%M').time()
        time_finish_book =  datetime.strptime(request.POST['time_finish_booking'], '%H:%M').time()
        description_book = request.POST['description_booking']

        # ищем объект комнаты
        room_object = Rooms.objects.get(id=id_room)
        # получаем объект даты
        date_book_object= DateBookingRoom.objects.get(room_fk=room_object,date=date_book)

        all_times = TimesBooking.objects.filter(date_fk=date_book_object)
        status_booking = '200'
        if is_time_available(time_start_book,time_finish_book,all_times):
            TimesBooking(time_start_booking=time_start_book,time_finish_booking= time_finish_book, user_fk=request.user,
                         date_fk=date_book_object, description_booking = description_book).save()
        else:
            status_booking = '500'

        # Получаем данные
        times_response = get_times_for_date(request, id_room, date_book)
        times_data = json.loads(times_response.content.decode('utf-8'))

        # Формируем ответ
        response_data = {
            'data': times_data,
            'status': status_booking
        }
        return JsonResponse(response_data)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('App:login'))