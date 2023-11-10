from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .models import Reservation, Cake
from . import views

class HomeView(TemplateView):
    template_name = 'index.html'

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user.html'

class ReservationListView(ListView):  
    model = Reservation  
    context_object_name = 'reservations'
    template_name = 'reservations.html'

    def get_queryset(self):
        
        return Reservation.objects.all()  

class CakeListView(ListView):
    model = Cake
    context_object_name = 'cakes'
    template_name = 'cake.html'

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['name', 'date', 'time', 'guests']
    template_name = 'reservation_form.html'
    success_url = '/reservations/'

class ReservationEditView(UpdateView):
    model = Reservation
    fields = ['name', 'date', 'time', 'guests']
    template_name = 'reservation_edit.html'
    success_url = '/reservations/'

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['name', 'date', 'time', 'guests']
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservations')

class ReservationEditView(UpdateView):
    model = Reservation
    fields = ['name', 'date', 'time', 'guests']
    template_name = 'reservation_edit.html'
    success_url = reverse_lazy('reservations')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations')