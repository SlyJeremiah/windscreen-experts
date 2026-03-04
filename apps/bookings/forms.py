from django import forms
from .models import Booking
from apps.services.models import Service

class BookingForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'service', 'vehicle_type', 'vehicle_make', 'vehicle_model', 'vehicle_year',
            'preferred_date', 'preferred_time', 'location', 'notes',
        ]
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tinashe'}),
            'last_name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Moyo'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'phone':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+263 77 000 0000'}),
            'service':      forms.Select(attrs={'class': 'form-select'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Toyota'}),
            'vehicle_model':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Corolla'}),
            'vehicle_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2020'}),
            'location':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address in Harare'}),
            'notes':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any extra details…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['vehicle_make'].required = False
        self.fields['vehicle_model'].required = False
        self.fields['vehicle_year'].required = False
        self.fields['notes'].required = False


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
