from django import forms
from .models import Reservation
from .models import Cake


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['datetime', 'size', 'batter', 'filling', 'special_request']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_request': forms.Textarea(attrs={'rows': 4}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)