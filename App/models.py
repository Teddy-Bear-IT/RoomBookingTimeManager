from django.db import models

# Import your models here.
from django.contrib.auth.models import User

# Create your models here.

class Rooms(models.Model):
    number_room = models.CharField(max_length=10)
    status_booking = models.BooleanField(default=False)

    def __str__(self):
        return f'Комната - {self.number_room}'
class DateBookingRoom(models.Model):
    room_fk = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'Дата - {self.date} | Комната - {self.room_fk.number_room}'
class TimesBooking(models.Model):
    time_start_booking = models.TimeField()
    time_finish_booking = models.TimeField()
    user_fk = models.ForeignKey( User,on_delete=models.CASCADE)
    date_fk = models.ForeignKey(DateBookingRoom,on_delete=models.CASCADE)
    description_booking = models.CharField(max_length=500,default='Без описания')

    def __str__(self):
        return f'{self.date_fk.room_fk} | {self.date_fk.date}  {self.time_start_booking}-{self.time_finish_booking}'

