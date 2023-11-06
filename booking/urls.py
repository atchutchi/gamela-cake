# booking/urls.py
from django.urls import path
from .views.reservation_views import ReservationListView
from .views.user_views import UserListView
from .views.cake_views import CakeListView

urlpatterns = [
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('cakes/', CakeListView.as_view(), name='cake_list'),
    # Adicione mais padrões de URL conforme necessário
]
