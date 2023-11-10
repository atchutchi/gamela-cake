# gamelacake/urls.py
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import SignUpView
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
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reservations/', ReservationListView.as_view(), name='reservation'),
    path('cakes/', CakeListView.as_view(), name='cake'),
    path('reservations/add/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/edit/<int:pk>/', ReservationEditView.as_view(), name='reservation_edit'),
    path('reservations/delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_delete'),
]