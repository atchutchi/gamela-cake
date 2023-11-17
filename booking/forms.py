from django import forms
from .models import Reservation
from .models import Cake


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['datetime', 'size', 'batter', 'filling', 'special_request', 'cake']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_request': forms.Textarea(attrs={'rows': 4}),
        }
