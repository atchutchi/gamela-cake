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
