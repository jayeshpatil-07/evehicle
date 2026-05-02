from django.contrib import admin
from .models import ChargingStation, Booking


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_active')
    search_fields = ('name', 'city')
    list_filter = ('city', 'is_active')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'station', 'date', 'time_slot', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'station__name')

from django.contrib import admin
from .models import LoginHistory

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "ip_address")
    list_filter = ("login_time",)
    search_fields = ("user__username",)
