from django.views.generic import (
    TemplateView, ListView, CreateView,
    UpdateView, DeleteView, DetailView
)
from django.views.generic.edit import FormView
from django import forms
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
import json
from .models import Cake, ContactMessage, Order, Reservation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm, ReservationForm, SignUpForm
import logging


# HomeView - Display the homepage
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_cakes = Cake.objects.all()[:4]
        context['cakes'] = featured_cakes
        context['form'] = ContactForm()
        return context


# login
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            messages.success(self.request, 'Login successful!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)


# SignUpView - Handle user registration
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# CakeListView - Display a list of cakes
class CakeListView(ListView):
    model = Cake
    context_object_name = 'cakes'
    template_name = 'cake.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Cake.objects.all()
        order = self.request.GET.get('order_by')
        filter_by = self.request.GET.get('filter_by')

        if filter_by:
            queryset = queryset.filter(name__icontains=filter_by)

        if order:
            queryset = queryset.order_by(order)

        return queryset


# OrderCreateView - Handle creation of new orders
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['cake', 'user']
    template_name = 'order_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        messages.success(
            self.request,
            'Your order has been successfully made.'
            )
        return super().form_valid(form)


# OrderListView - Display a list of user's orders
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# OrderDetailView - Display details of a specific order
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'review_order.html'

    def get_queryset(self):
        # Ensures that users can only access their own orders
        return Order.objects.filter(reservation__user=self.request.user)


# OrderDeleteView - Handle deletion of orders
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


# contact - Handle contact form submissions
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# MakeReservationView - Handle creation of new reservations
class MakeReservationView(LoginRequiredMixin, View):
    def post(self, request, cake_id):
        cake = get_object_or_404(Cake, pk=cake_id)
        user = request.user

        # Create booking
        reservation = Reservation.objects.create(
            user=user,
            cake=cake,
            datetime=timezone.now()
        )

        # Create a corresponding order
        order = Order.objects.create(
            user=user,
            cake=cake,
            reservation=reservation
        )

        # Send email confirmation
        send_mail(
            'Booking Confirmation',
            'Your reservation was successful.',
            'ferreira.atchutchi@gmail.com',
            [user.email],
            fail_silently=False,
        )

        # Add success message
        messages.success(request, 'Cake booked successfully!')

        return redirect('reservations')


# UserReservationListView - Display a list of user's reservations
class UserReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        ).order_by('-datetime')


# UserView - Display user profile and reservations
class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['upcoming_reservations'] = Reservation.objects.filter(
            user=user, datetime__gte=timezone.now()).order_by('datetime')
        context['past_reservations'] = Reservation.objects.filter(
            user=user, datetime__lt=timezone.now()).order_by('-datetime')
        return context


# Create reservation
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservations')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.save()
        messages.success(self.request, "Reservation successfully created!")
        return super().form_valid(form)


class ReservationCancelForm(forms.Form):
    """Formulário vazio, usado apenas para manter o padrão de FormView."""
    pass


# delete reservation
class ReservationDeleteView(LoginRequiredMixin, FormView):
    template_name = 'reservation_confirm_delete.html'
    form_class = ReservationCancelForm
    success_url = reverse_lazy('reservations')

    def form_valid(self, form):
        reservation_id = self.kwargs.get('pk')
        reservation = get_object_or_404(
            Reservation, pk=reservation_id, user=self.request.user
        )

        if reservation.can_cancel():
            reservation.delete()
            messages.success(
                self.request, "Reservation successfully cancelled.")
        else:
            messages.error(
                self.request,
                "Reservation cannot be cancelled within 24 hours."
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservation'] = get_object_or_404(
            Reservation, pk=self.kwargs.get('pk')
        )
        return context


# edit reservation
class ReservationEditView(LoginRequiredMixin, UpdateView):
    model = Reservation
    fields = ['cake', 'datetime']
    template_name = 'reservation_edit.html'
    success_url = reverse_lazy('reservations')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        if reservation.can_cancel():
            reservation.save()
            messages.success(self.request, "Reservation successfully updated.")
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                "Reservations editable only if over 24 hours in advance."
                )
            return HttpResponseRedirect(reverse('reservations'))

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservation_detail.html'

    def get_queryset(self):
        # users can only access their own reservations
        return Reservation.objects.filter(user=self.request.user)
