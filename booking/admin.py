from django.contrib import admin
from .models import Cake, Reservation, Order  # Import the models to be used in the admin site

# Admin configuration for the Cake model
@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']  # Specify the fields to display in the admin list view
    search_fields = ['name']  # Enable search functionality for the 'name' field

# Admin configuration for the Reservation model
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'time']  # Define which fields are shown in the list view
    list_filter = ['date', 'time']  # Provide filter options in the sidebar for 'status' and 'date_time'

# Admin configuration for the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cake', 'reservation', 'quantity']  # Fields to be displayed in the list view
    list_filter = ['reservation']  # Sidebar filter based on 'reservation'
