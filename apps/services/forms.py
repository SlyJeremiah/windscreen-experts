from django import forms
from .models import Service, ServicePricing

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'slug', 'description', 'short_description', 'icon', 'is_active', 'order']
        widgets = {
            'name':              forms.TextInput(attrs={'class': 'form-control'}),
            'slug':              forms.TextInput(attrs={'class': 'form-control'}),
            'description':       forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'icon':              forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-tools'}),
            'order':             forms.NumberInput(attrs={'class': 'form-control'}),
        }

ServicePricingFormSet = forms.inlineformset_factory(
    Service, ServicePricing,
    fields=['vehicle_type', 'label', 'price', 'is_starting_price'],
    extra=2, can_delete=True,
    widgets={
        'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
        'label':        forms.TextInput(attrs={'class': 'form-control'}),
        'price':        forms.NumberInput(attrs={'class': 'form-control'}),
    }
)
