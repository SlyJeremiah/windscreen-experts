from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model  = GalleryItem
        fields = [
            'title', 'service', 'media_type',
            'before_image', 'after_image',
            'video', 'video_thumbnail',
            'description', 'vehicle_type', 'is_featured', 'order',
        ]
        widgets = {
            'title':           forms.TextInput(attrs={'class': 'form-control'}),
            'service':         forms.Select(attrs={'class': 'form-select'}),
            'media_type':      forms.Select(attrs={'class': 'form-select', 'id': 'id_media_type'}),
            'description':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vehicle_type':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sedan'}),
            'order':           forms.NumberInput(attrs={'class': 'form-control'}),
        }
