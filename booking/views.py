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
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ReservationForm

class HomeView(TemplateView):
    template_name = 'index.html'

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        current_time = timezone.now()
        context['upcoming_reservations'] = Reservation.objects.filter(user=user, datetime__gte=current_time)
        context['past_reservations'] = Reservation.objects.filter(user=user, datetime__lt=current_time)
        return context

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

        # Ensure this matches the field name in your form        
        desired_time = form.cleaned_data['datetime']  # Ensure this matches the field name in your form

        # Check if the reservation time slot is already booked
        if Reservation.objects.filter(
            Q(datetime__gte=desired_time - timedelta(hours=2),
              datetime__lte=desired_time + timedelta(hours=2))
        ).exclude(pk=self.object.pk if self.object else None).exists():
            form.add_error('datetime', 'This time slot is already booked. Please choose another time.')
            messages.error(self.request, 'This time slot is already booked. Please choose another time.')
            return self.form_invalid(form)

        # Assign the current user to the reservation before saving
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.save()

        # Add a success message
        messages.success(self.request, 'Your reservation has been successfully made.')
        return super().form_valid(form)



class ReservationEditView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_edit.html'
    success_url = reverse_lazy('reservation')

    def form_valid(self, form):
        # Cutoff time for modifications (e.g. 24 hours in advance)
        cutoff_time = timedelta(hours=24)

        # Check if the reservation is within the cut-off time
        if timezone.now() >= self.object.datetime - cutoff_time:
            messages.error(self.request, "It's too late to modify this reservation.")
            return redirect('reservation')

        # Continue with the update if it is outside the cutoff time
        messages.success(self.request, "Your reservation has been successfully updated.")
        return super().form_valid(form)

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

class ReservationCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        cutoff_time = timedelta(hours=24)

        if timezone.now() <= reservation.datetime - cutoff_time:
            reservation.delete()
            send_mail(
                'Reservation Cancellation Confirmation',
                'Your reservation has been successfully cancelled.',
                'ferreira.atchutchi@gmail.com',  # admin email
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, 'Reservation cancelled successfully.')
        else:
            messages.error(request, "It's too late to cancel this reservation.")
        return redirect('reservation')