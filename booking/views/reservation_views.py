# booking/views/reservation_views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Reservation

class ReservationListView(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'reservations/reservation_list.html'

class ReservationDetailView(DetailView):
    model = Reservation
    context_object_name = 'reservation'
    template_name = 'reservations/reservation_detail.html'

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['user', 'date', 'time', 'party_size', 'special_request']
    template_name = 'reservations/reservation_form.html'

class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = ['date', 'time', 'party_size', 'special_request']
    template_name = 'reservations/reservation_form.html'

class ReservationDeleteView(DeleteView):
    model = Reservation
    context_object_name = 'reservation'
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = '/reservations/'
