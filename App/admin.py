from django.contrib import admin

# import  your models here.

from .models import  Rooms,DateBookingRoom,TimesBooking


# Register your models here.

admin.site.register(Rooms)
admin.site.register(DateBookingRoom)
admin.site.register(TimesBooking)
