from django.contrib import admin
from .models import Cake, Order, Reservation # Import the models to be used in the admin site

# Admin configuration for the Cake model
@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']  # Specify the fields to display in the admin list view
    search_fields = ['name']  # Enable search functionality for the 'name' field


# Admin configuration for the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cake', 'reservation']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'cake', 'datetime']