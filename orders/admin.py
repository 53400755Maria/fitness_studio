from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'booking_date', 'booking_time', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'service__title')