from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from .views import SignUpView, CakeListView, OrderCreateView, OrderListView, OrderDetailView, OrderDeleteView, contact, MakeReservationView, UserReservationListView, ReservationCreateView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cakes/', CakeListView.as_view(), name='cake'),
    path('order/add/', OrderCreateView.as_view(), name='order_create'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('contact/', contact, name='contact'),
    path('reserve/<int:cake_id>/', MakeReservationView.as_view(), name='make_reservation'),
    path('reservations/', UserReservationListView.as_view(), name='reservations'),
    path('users/', views.UserView.as_view(), name='user'),
    path('reservations/create/<int:cake_id>/', ReservationCreateView.as_view(), name='reservation_create'),
]
