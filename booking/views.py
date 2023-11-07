from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .models import Reservation, Cake
from . import views

class HomeView(TemplateView):
    template_name = 'index.html'

class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user.html'

class ReservationListView(ListView):  
    model = Reservation  
    context_object_name = 'reservations'
    template_name = 'reservation.html'

    def get_queryset(self):
        
        return Reservation.objects.all()  

class CakeListView(ListView):
    model = Cake
    context_object_name = 'cakes'
    template_name = 'cake.html'
