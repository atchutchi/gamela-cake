from django.contrib import admin
from .models import Cake, Order, Reservation  # Import models for admin site


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    # Specify fields to display in admin list view
    list_display = ['name', 'price']
    # Enable search functionality for the 'name' field
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cake', 'reservation']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'cake', 'datetime']
