from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'service', 'before_image', 'after_image', 'description', 'vehicle_type', 'is_featured', 'order']
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'service':      forms.Select(attrs={'class': 'form-select'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sedan'}),
            'order':        forms.NumberInput(attrs={'class': 'form-control'}),
        }
