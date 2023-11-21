from django.urls import path, include
from . import views
from .views import (
    SignUpView, CakeListView, OrderCreateView, OrderListView,
    OrderDetailView, OrderDeleteView, contact,
    MakeReservationView, UserReservationListView, ReservationCreateView,
    CustomLoginView
)

urlpatterns = [
    # Home page of the site
    path('', views.HomeView.as_view(), name='home'),

    # User login page
    path('login/', CustomLoginView.as_view(), name='login'),

    # User registration page
    path('signup/', SignUpView.as_view(), name='signup'),

    # Include default authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # List of available cakes
    path('cakes/', CakeListView.as_view(), name='cake'),

    # Page to create a new order
    path('order/add/', OrderCreateView.as_view(), name='order_create'),

    # User's list of orders
    path('order/list/', OrderListView.as_view(), name='order_list'),

    # Details of a specific order
    path('order/detail/<int:pk>/', OrderDetailView.as_view(),
         name='order_detail'),

    # Delete an existing order
    path('order/delete/<int:pk>/', OrderDeleteView.as_view(),
         name='order_delete'),

    # Contact page
    path('contact/', views.contact, name='contact'),

    # Reserve a specific cake
    path('reserve/<int:cake_id>/', MakeReservationView.as_view(),
         name='make_reservation'),

    # User's list of reservations
    path('reservations/', UserReservationListView.as_view(),
         name='reservations'),

    # User profile page
    path('users/', views.UserView.as_view(), name='user'),

    # Create a new reservation
    path('reservations/create/<int:cake_id>/',
         ReservationCreateView.as_view(), name='reservation_create'),

    # Delete an existing reservation
    path('reservations/delete/<int:pk>/',
         views.ReservationDeleteView.as_view(), name='reservation_delete'),

    # Edit an existing reservation
    path('reservations/edit/<int:pk>/',
         views.ReservationEditView.as_view(), name='reservation_edit'),

    # Create a new reservation in reservations.html
    path('reservations/new/', ReservationCreateView.as_view(),
         name='new_reservation'),
]
