from django import forms
from .models import Reservation
from .models import Cake


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
        )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
        )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone'})
        )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Message'})
        )


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['cake', 'datetime']
        widgets = {
            'cake': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Your Cake'}),
            'datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Pick a Date and Time', 'type': 'datetime-local'}),
        }
        labels = {
            'cake': False,
            'datetime': False,
        }