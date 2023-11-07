# gamelacake/urls.py
from django.urls import path
from booking.views import HomeView, UserListView, ReservationListView, CakeListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('cakes/', CakeListView.as_view(), name='cake_list'),
    # ... outras URLs
]
