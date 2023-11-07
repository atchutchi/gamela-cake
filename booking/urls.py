# gamelacake/urls.py
from django.urls import path
from booking.views import (
    HomeView,
    UserListView,
    ReservationListView,
    ReservationCreateView,
    ReservationEditView,
    ReservationDeleteView,
    CakeListView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('users/', UserListView.as_view(), name='user'),
    path('reservations/', ReservationListView.as_view(), name='reservation'),
    path('cakes/', CakeListView.as_view(), name='cake'),
    path('reservations/add/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/edit/<int:pk>/', ReservationEditView.as_view(), name='reservation_edit'),
    path('reservations/delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_delete'),
]