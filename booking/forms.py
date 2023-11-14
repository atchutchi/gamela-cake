from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['datetime', 'size', 'batter', 'filling', 'special_request']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_request': forms.Textarea(attrs={'rows': 4}),
        }
