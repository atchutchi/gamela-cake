from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Reservation, Cake
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .forms import ReservationForm

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
    paginate_by = 10  # control cakes per pages

    def get_queryset(self):
        queryset = Cake.objects.all()
        order = self.request.GET.get('order_by')
        filter_by = self.request.GET.get('filter_by')

        if filter_by:
            queryset = queryset.filter(name__icontains=filter_by)

        if order:
            queryset = queryset.order_by(order)

        return queryset

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservation')
    
    def form_valid(self, form):
        desired_time = form.cleaned_data['datetime']  # Ensure this matches the field name in your form

        if Reservation.objects.filter(
            Q(datetime__gte=desired_time - timedelta(hours=2),
            datetime__lte=desired_time + timedelta(hours=2))
        ).exclude(pk=self.object.pk if self.object else None).exists():
            form.add_error('datetime', 'This time slot is already booked. Please choose another time.')
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationEditView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_edit.html'
    success_url = reverse_lazy('reservations')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations')

def get_available_slots(request):
    date = request.GET.get('date')  
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    
    # time slots
    slots = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    booked_slots = Reservation.objects.filter(datetime__date=date).values_list('datetime__time', flat=True)
    available_slots = [slot for slot in slots if slot not in booked_slots]

    return JsonResponse({'available_slots': available_slots})