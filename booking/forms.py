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
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
